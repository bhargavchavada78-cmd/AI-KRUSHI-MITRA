
from pathlib import Path
from datetime import datetime
import shutil
import uuid

from PIL import Image, UnidentifiedImageError

from deep_learning.crop_health import predict_crop_health
from database.connection import get_connection


# ------------------------------------------
# 1. Configuration
# ------------------------------------------

UPLOAD_DIR = Path("datasets/farmer_uploads")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------
# 2. Helper: determine image extension
# ------------------------------------------

def get_image_extension(image_file):
    """
    Accept a file path or an uploaded file object.
    Return a safe image extension.
    """

    filename = getattr(image_file, "name", "")

    if not filename and isinstance(image_file, (str, Path)):
        filename = str(image_file)

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported image format. "
            "Use JPG, JPEG, PNG, or WEBP."
        )

    return extension


# ------------------------------------------
# 3. Helper: validate and save image
# ------------------------------------------

def save_crop_image(crop_id, image_file):
    """
    Validate an image and save it using a unique filename.
    Returns saved image path.
    """

    extension = get_image_extension(image_file)

    # Read the image bytes without trusting its filename.
    if isinstance(image_file, (str, Path)):
        source_path = Path(image_file)

        if not source_path.is_file():
            raise FileNotFoundError("Image file not found.")

        if source_path.stat().st_size > MAX_FILE_SIZE:
            raise ValueError("Image must be 10 MB or smaller.")

        with Image.open(source_path) as image:
            image.verify()

        with open(source_path, "rb") as file:
            image_bytes = file.read()

    else:
        # Supports file-like objects such as BytesIO.
        if hasattr(image_file, "getvalue"):
            image_bytes = image_file.getvalue()
        else:
            if hasattr(image_file, "seek"):
                image_file.seek(0)

            image_bytes = image_file.read()

        if not image_bytes:
            raise ValueError("The image file is empty.")

        if len(image_bytes) > MAX_FILE_SIZE:
            raise ValueError("Image must be 10 MB or smaller.")

        from io import BytesIO

        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()

    # Use a random name to avoid overwriting previous images.
    filename = (
        f"crop_{crop_id}_{uuid.uuid4().hex}{extension}"
    )

    destination = UPLOAD_DIR / filename

    with open(destination, "wb") as file:
        file.write(image_bytes)

    return destination


# ------------------------------------------
# 4. Helper: confidence category
# ------------------------------------------

def get_confidence_level(confidence):
    """
    These are prototype confidence thresholds,
    not measurements of disease severity.
    """

    if confidence >= 0.80:
        return "High"

    if confidence >= 0.60:
        return "Medium"

    return "Low"


# ------------------------------------------
# 5. Main service
# ------------------------------------------

def save_health_check(crop_id, image_file):
    """
    1. Validate and save the image.
    2. Run CNN prediction.
    3. Save image and analysis records in MySQL.
    4. Return the analysis result.
    """

    if not isinstance(crop_id, int) or crop_id <= 0:
        raise ValueError("crop_id must be a positive integer.")

    saved_path = None
    connection = None
    cursor = None

    try:
        # Step A: save and validate image.
        saved_path = save_crop_image(crop_id, image_file)

        # Step B: open and predict using the CNN.
        with Image.open(saved_path) as image:
            image = image.convert("RGB")
            predicted_class, confidence = predict_crop_health(
                image
            )

        # Ensure a valid probability from the model.
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("CNN returned an invalid confidence.")

        confidence_percent = round(confidence * 100, 2)
        confidence_level = get_confidence_level(confidence)

        # Step C: insert records using one transaction.
        connection = get_connection()
        connection.start_transaction()
        cursor = connection.cursor()

        image_query = """
            INSERT INTO crop_images
                (crop_id, image_path, capture_date)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            image_query,
            (
                crop_id,
                str(saved_path),
                datetime.now()
            )
        )

        image_id = cursor.lastrowid

        # Match the actual health_analysis schema.
        analysis_query = """
            INSERT INTO health_analysis
                (image_id, prediction, confidence,
                 severity, analysis_date)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            analysis_query,
            (
                image_id,
                predicted_class,
                confidence_percent,
                confidence_level,
                datetime.now()
            )
        )

        analysis_id = cursor.lastrowid

        # Commit both records together.
        connection.commit()

        return {
            "success": True,
            "crop_id": crop_id,
            "image_id": image_id,
            "analysis_id": analysis_id,
            "prediction": predicted_class,
            "confidence": confidence_percent,
            "confidence_level": confidence_level,
            "image_path": str(saved_path),
            "message": "Crop image analyzed and saved."
        }

    except Exception:
        if connection is not None and connection.is_connected():
            connection.rollback()

        # Remove the saved file if the database operation failed.
        if saved_path is not None and saved_path.exists():
            saved_path.unlink()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

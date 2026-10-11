
from pathlib import Path
import json
import numpy as np
from PIL import Image
from tensorflow import keras


# --------------------------------
# 1. Model and class-name paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "cotton_cnn.keras"
CLASS_PATH = BASE_DIR / "models" / "class_names.json"

IMAGE_SIZE = (180, 180)

# Load the model only when the first prediction is requested.
_model = None
_class_names = None


# --------------------------------
# 2. Load model and class names
# --------------------------------

def load_crop_model():
    global _model, _class_names

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"CNN model not found: {MODEL_PATH}"
            )

        if not CLASS_PATH.exists():
            raise FileNotFoundError(
                f"Class names file not found: {CLASS_PATH}"
            )

        _model = keras.models.load_model(MODEL_PATH)

        with open(CLASS_PATH, "r", encoding="utf-8") as file:
            _class_names = json.load(file)

        if not isinstance(_class_names, list):
            raise ValueError(
                "class_names.json must contain a list."
            )

    return _model, _class_names


# --------------------------------
# 3. Predict crop health
# --------------------------------

def predict_crop_health(image):
    """
    Accepts a PIL image or image file path.

    Returns:
        predicted_class: str
        confidence: float between 0 and 1
    """

    model, class_names = load_crop_model()

    # Support both uploaded PIL images and file paths.
    if isinstance(image, Image.Image):
        img = image.copy()
    else:
        with Image.open(image) as opened_image:
            img = opened_image.copy()

    # Use the same image size and preprocessing
    # as deep_learning/predict.py.
    img = img.convert("RGB")
    img = img.resize(IMAGE_SIZE)

    image_array = np.asarray(img, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)[0]

    if len(predictions) != len(class_names):
        raise ValueError(
            "Model output count does not match class names."
        )

    predicted_index = int(np.argmax(predictions))
    predicted_class = class_names[predicted_index]
    confidence = float(predictions[predicted_index])

    return predicted_class, confidence
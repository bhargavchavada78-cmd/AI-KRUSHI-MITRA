from pathlib import Path
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras


# -----------------------------
# 1. Paths
# -----------------------------

MODEL_PATH = Path("deep_learning/models/cotton_cnn.keras")
CLASS_PATH = Path("deep_learning/models/class_names.json")


# -----------------------------
# 2. Load model
# -----------------------------

model = keras.models.load_model(MODEL_PATH)


# -----------------------------
# 3. Load class names
# -----------------------------

with open(CLASS_PATH, "r") as file:
    class_names = json.load(file)

print("Classes:", class_names)


# -----------------------------
# 4. Prediction function
# -----------------------------

def predict_leaf(image_path):

    # Load image
    image = keras.utils.load_img(
        image_path,
        target_size=(180, 180)
    )

    # Convert image to NumPy array
    image_array = keras.utils.img_to_array(image)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Model prediction
    predictions = model.predict(image_array, verbose=0)

    # Highest probability class
    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = float(predictions[0][predicted_index])

    return predicted_class, confidence


# -----------------------------
# 5. Test prediction
# -----------------------------

if __name__ == "__main__":

    image_path = input(
        "Enter cotton leaf image path: "
    ).strip()

    if not Path(image_path).exists():
        print("Image not found!")
    else:

        predicted_class, confidence = predict_leaf(
            image_path
        )

        print("\n-----------------------------")
        print("CROP HEALTH RESULT")
        print("-----------------------------")

        print("Predicted condition:", predicted_class)
        print(
            "Confidence:",
            f"{confidence * 100:.2f}%"
        )
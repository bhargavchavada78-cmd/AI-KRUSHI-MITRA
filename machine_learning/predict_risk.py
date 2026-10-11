
from pathlib import Path
import joblib
import pandas as pd

# Find the saved model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "cotton_risk_model.pkl"

FEATURES = [
    "day_of_year",
    "avg_temp_c",
    "avg_humidity_pct",
    "rainfall_mm",
    "leaf_wetness_hours",
    "wind_speed_kmph",
    "soil_moisture_pct",
    "prior_regional_incidence_pct"
]


def predict_risk(crop_data):
    # Check whether model exists
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    # Load the trained model
    model = joblib.load(MODEL_PATH)

    # Check required inputs
    missing = [
        feature for feature in FEATURES
        if feature not in crop_data
    ]

    if missing:
        raise ValueError(
            f"Missing input features: {missing}"
        )

    # Convert input into a DataFrame
    input_data = pd.DataFrame(
        [[crop_data[f] for f in FEATURES]],
        columns=FEATURES
    )

    if input_data.isnull().any().any():
        raise ValueError("Input values cannot be empty.")

    # Predict risk category
    prediction = model.predict(input_data)[0]

    # Get probability estimates, if available
    probabilities = model.predict_proba(input_data)[0]
    confidence = float(max(probabilities)) * 100

    return {
        "crop": "Cotton",
        "predicted_risk": str(prediction),
        "model_confidence_percent": round(confidence, 2),
        "experimental_model": True
    }



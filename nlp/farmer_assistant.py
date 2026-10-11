from database.queries import (
    get_full_crop_status,
    get_latest_weather,
    get_farm
)

def detect_intent(message):
    """Recognize the farmer's question."""
    text = message.lower().strip()

    intents = {
        "crop_stage": [
            "crop age", "growth stage",
            "crop stage", "how old", "growth"
        ],
        "weather": [
            "weather", "rain", "rainfall",
            "temperature", "humidity"
        ],
        "watering": [
            "water", "watering", "irrigation"
        ],
        "disease": [
            "disease", "leaf problem",
            "yellow leaves", "spots", "infection"
        ],
        "harvesting": [
            "harvest", "harvesting", "cut crop"
        ]
    }

    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "unknown"


def ask_farmer_assistant(
    message,
    crop_id=None,
    farm_id=None
):
    """Answer using stored farm data where available."""

    if not message or not message.strip():
        return "Please enter a question."

    intent = detect_intent(message)

    # Actual crop information from MySQL
    if intent == "crop_stage":
        if crop_id is None:
            return "Please select a crop first."

        crop = get_full_crop_status(crop_id)

        if crop is None:
            return "Crop not found in the database."

        return (
            f"Your {crop['crop_name']} crop is "
            f"{crop['crop_age']} days old. "
            f"The estimated growth stage is "
            f"{crop['stage']}."
        )

    # Actual latest stored weather from MySQL
    if intent == "weather":
        if farm_id is None:
            return "Please select your farm first."

        weather = get_latest_weather(farm_id)

        if weather is None:
            return (
                "No weather record is available. "
                "Update the farm weather first."
            )

        return (
            f"Latest stored weather: "
            f"Temperature: {weather[3]}, "
            f"Humidity: {weather[4]}, "
            f"Rainfall: {weather[5]}, "
            f"Rain probability: {weather[6]}."
        )

    if intent == "watering":
        return (
            "Check your soil moisture, crop stage, "
            "recent rainfall and local forecast before "
            "irrigating."
        )

    if intent == "disease":
        return (
            "Upload a clear photo in Crop Health Check. "
            "Confirm the suspected disease before choosing "
            "a pesticide or treatment."
        )

    if intent == "harvesting":
        return (
            "Harvest timing depends on crop variety, "
            "maturity signs and local conditions. "
            "Check crop-specific harvesting guidance."
        )

    return (
        "I can help with crop growth, weather, watering, "
        "leaf problems and harvesting."
    )


if __name__ == "__main__":
    # Replace these with IDs that exist in your database.
    CROP_ID = 1
    FARM_ID = 1

    questions = [
        "What is my crop health?",
        "What is the latest weather?"
    ]

    for question in questions:
        print("\nFarmer:", question)
        print(
            "Assistant:",
            ask_farmer_assistant(
                question,
                crop_id=CROP_ID,
                farm_id=FARM_ID
            )
        )


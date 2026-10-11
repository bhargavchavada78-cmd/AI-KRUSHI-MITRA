import requests


def get_coordinates(location):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "IN"
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"Location not found: {location}")

    result = data["results"][0]

    return result["latitude"], result["longitude"]
def get_weather(location):

    latitude, longitude = get_coordinates(location)

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "rain,"
            "precipitation"
        ),

        "hourly": (
            "precipitation_probability,"
            "rain"
        ),

        "forecast_days": 1,

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    rain_probabilities = data["hourly"]["precipitation_probability"]

    next_6_hours_probability = max(
        rain_probabilities[:6]
    )

    return {
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rainfall": current["rain"],
        "precipitation": current["precipitation"],
        "rain_probability": next_6_hours_probability
    }

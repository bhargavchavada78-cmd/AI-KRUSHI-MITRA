from datetime import date

from weather.weather_service import get_weather
from database.queries import add_weather


# Get live weather for farm location
weather = get_weather("Sami")


# Save weather into MySQL
add_weather(
    farm_id=1,
    weather_date=date.today(),
    temperature=weather["temperature"],
    humidity=weather["humidity"],
    rainfall=weather["rainfall"],
    rain_probability=weather["rain_probability"]
)


print("Live weather saved to SQL!")
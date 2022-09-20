import requests
import api_key

#city_name = "Warsaw"
#units = "metric"


def get_weather_by_city_name(self, city_name: str, country_code: str, units: str):
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key.API_KEY}&units={units}")
    return weather_response




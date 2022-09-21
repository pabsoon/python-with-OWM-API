import requests
from PyQt5.QtGui import QImage

import api_key


# city_name = "Warsaw"
# units = "metric"


def get_weather_by_city_name(self, city_name: str, country_code: str, units: str):
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key.API_KEY}&units={units}")
    return weather_response


def get_weather_image(self, code: str):
    image_response = requests.get(f"https://openweathermap.org/img/wn/{code}@2x.png")
    image = QImage()
    image.loadFromData(image_response.content)
    return image

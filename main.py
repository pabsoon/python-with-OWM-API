import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic

import config
import owmAPI


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("WeatherAppGui.ui", self)

        self.get_data_btn = self.findChild(QPushButton, "getDataBtn")
        self.image_label = self.findChild(QLabel, "imageLabel")
        self.temp_label = self.findChild(QLabel, "tempLabel")
        self.details_box = self.findChild(QGroupBox, "detailsBox")
        self.description_label = self.findChild(QLabel, "descriptionLabel")
        self.feels_like_label = self.findChild(QLabel, "feelsLikeLabel")
        self.pressure_label = self.findChild(QLabel, "pressureLabel")
        self.humidity_label = self.findChild(QLabel, "humidityLabel")
        self.wind_label = self.findChild(QLabel, "windLabel")
        self.clouds_label = self.findChild(QLabel, "cloudsLabel")
        self.save_button = self.findChild(QPushButton, "saveButton")
        self.line_edit_api_key = self.findChild(QLineEdit, "lineEditApiKey")

        self.get_data_btn.clicked.connect(self.get_data)
        self.save_button.clicked.connect(lambda: owmAPI.save_changed_config(5, self.line_edit_api_key.text(), 'metric'))
        self.line_edit_api_key.setText(config.API_KEY)

    def get_data(self):
        weather_response = owmAPI.get_weather_by_city_name(self, "Warsaw", "PL", "metric")
        weather_json = weather_response.json()
        code = weather_json["weather"][0]["icon"]
        temperature = weather_json["main"]["temp"]
        country_name = weather_json["name"]
        country_code = weather_json["sys"]["country"]
        description = weather_json["weather"][0]["description"]
        feels_like = weather_json["main"]["feels_like"]
        pressure = weather_json["main"]["pressure"]
        humidity = weather_json["main"]["humidity"]
        wind = weather_json["wind"]["speed"]
        clouds = weather_json["clouds"]["all"]

        image = owmAPI.get_weather_image(self, code)
        self.details_box.setTitle(f"{country_name}, {country_code}")
        self.image_label.setPixmap(QPixmap(image))
        self.temp_label.setText(f"{temperature}°")
        self.description_label.setText(f"{description}")
        self.feels_like_label.setText(f"{feels_like}°")
        self.pressure_label.setText(f"{pressure} hPa")
        self.humidity_label.setText(f"{humidity} %")
        self.wind_label.setText(f"{wind}")
        self.clouds_label.setText(f"{clouds} %")

        pass


app = QApplication(sys.argv)

window = WeatherApp()
window.show()
owmAPI.check_config(window)
app.exec_()

import os

import requests
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QLineEdit, QTabWidget, QMessageBox

import config

CONF_FILE = "config.py"


def get_weather_by_city_name(self, city_name: str, country_code: str, units: str):
    check_config(self)
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={config.API_KEY}&units={units}")

    return weather_response


def get_weather_image(self, code: str):
    image_response = requests.get(f"https://openweathermap.org/img/wn/{code}@2x.png")
    image = QImage()
    image.loadFromData(image_response.content)
    return image


def check_config(self):
    self.line_edit_key = self.findChild(QLineEdit, "lineEditKey")
    self.tab_widget = self.findChild(QTabWidget, "tabWidget")
    if check_if_config_exists() is not True:
        file = open(CONF_FILE, "a")
        file.write("API_KEY = ''\nREFRESH_TIME = 5\nUNITS = 'metric'\n")
    elif len(config.API_KEY) < 31:
        self.tab_widget.setCurrentIndex(1)
        show_pop_up("Warning", "Please paste your API Key in Settings Tab", QMessageBox.Critical)
    else:
        # TODO timer
        self.tab_widget.setCurrentIndex(0)


def show_pop_up(title: str, text: str, icon: QMessageBox.Icon):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec_()


def check_if_config_exists():
    return os.path.isfile(CONF_FILE)


def save_changed_config(self, refresh_time: int, api_key: str, units: str):
    if refresh_time != config.REFRESH_TIME:
        config.REFRESH_TIME = refresh_time
    if api_key != config.API_KEY:
        config.API_KEY = api_key
    if units != config.UNITS:
        config.UNITS = units

from configparser import ConfigParser
from os.path import exists

import requests
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox

CONF_FILE = "Files/config.ini"


def show_pop_up(title: str, text: str, icon: QMessageBox.Icon):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec_()


def get_weather_by_city_name(self, city_name: str, country_code: str):
    if check_config_file(self):
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name},"
            f"{country_code}&appid={read_config('API_KEY')}&units={read_config('UNITS')}")
        print("API refreshed")

        return res.json()
    else:
        show_pop_up("ERROR API", "Incorrect config file!!\nDelete it and run app again", QMessageBox.Critical)
        return False


def get_weather_image(code: str):
    image_response = requests.get(f"https://openweathermap.org/img/wn/{code}@2x.png")
    image = QImage()
    image.loadFromData(image_response.content)
    return image


def check_config_file(self):
    if exists(CONF_FILE):
        __api_key = read_config('API_KEY')
        __refresh_time = int(read_config('REFRESH_TIME'))
        __units = read_config('UNITS')
        if len(__api_key) != 32:
            print("Incorrect API_KEY")
            self.tab_widget.setCurrentIndex(1)
            show_pop_up("Warning", "Please paste correct API Key in Settings Tab", QMessageBox.Warning)
            return False
        if __refresh_time < 1 or __refresh_time > 1000:
            print(f'value {__refresh_time} is not between 1 and 1000')
            return False
        if __units == 'metric' or __units == 'imperial':

            return True
        else:
            print(f'{__units} is not proper value for units')
            return False
    else:
        create_config('', 5, 'metric')
        print('created template config')
        return False


def create_config(api_key: str, refresh_time: int, units: str):
    config = ConfigParser()
    config.read(CONF_FILE)
    if not config.has_section('main'):
        config.add_section('main')
    config.set('main', 'API_KEY', f'{api_key}')
    config.set('main', 'REFRESH_TIME', f'{refresh_time}')
    config.set('main', 'UNITS', f'{units}')

    with open(CONF_FILE, 'w') as file:
        config.write(file)


def save_config(api_key: str, refresh_time: int, units: str):
    if api_key == "" or api_key is None or len(api_key) != 32:
        show_pop_up("Error!", "!!Bad API Key!!", QMessageBox.Critical)
    else:
        create_config(api_key, refresh_time, units)


def read_config(key_name: str):
    config = ConfigParser()
    config.read(CONF_FILE)
    value = config.get('main', f'{key_name}')

    return value

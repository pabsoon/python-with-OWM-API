import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")
        self.tab_widget.setCurrentIndex(0)
        self.get_data_btn.clicked.connect(self.set_data)
        self.save_button.clicked.connect(lambda: owmAPI.save_config(self.line_edit_api_key.text(), 5, 'metric'))
        self.line_edit_api_key.setText(owmAPI.read_config('API_KEY'))

    def set_data(self):
        data = owmAPI.get_weather_by_city_name(self, "Warsaw", "PL")
        if data != False:
            units = '', ''
            if owmAPI.read_config('UNITS') == 'metric':
                units = '°C', 'm/s'
            else:
                units = '°F', 'm/h'
            image = owmAPI.get_weather_image(data["weather"][0]["icon"])
            self.details_box.setTitle(f'{data["name"]} {data["sys"]["country"]}')
            self.image_label.setPixmap(QPixmap(image))
            self.temp_label.setText(f'{data["main"]["temp"]}{units[0]}')
            self.description_label.setText(f'{data["weather"][0]["description"]}')
            self.feels_like_label.setText(f'{data["main"]["feels_like"]}{units[0]}')
            self.pressure_label.setText(f'{data["main"]["pressure"]}hPa')
            self.humidity_label.setText(f'{data["main"]["humidity"]}%')
            self.wind_label.setText(f'{data["wind"]["speed"]}{units[1]}')
            self.clouds_label.setText(f'{data["clouds"]["all"]}%')


app = QApplication(sys.argv)

window = WeatherApp()

window.show()
#owmAPI.check_config_file(window)
if owmAPI.check_config_file(window):
    QTimer.singleShot(1, lambda: window.set_data())
    timer = QTimer()
    timer.timeout.connect(lambda: window.set_data())
    timer.setInterval(int(owmAPI.read_config("refresh_time")) * 1000)
    timer.start()


sys.exit(app.exec_())

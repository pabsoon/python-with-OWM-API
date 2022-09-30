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

        self.image_label = self.findChild(QLabel, "imageLabel")
        self.temp_label = self.findChild(QLabel, "tempLabel")
        self.description_label = self.findChild(QLabel, "descriptionLabel")
        self.feels_like_label = self.findChild(QLabel, "feelsLikeLabel")
        self.pressure_label = self.findChild(QLabel, "pressureLabel")
        self.humidity_label = self.findChild(QLabel, "humidityLabel")
        self.wind_label = self.findChild(QLabel, "windLabel")
        self.clouds_label = self.findChild(QLabel, "cloudsLabel")

        self.get_data_btn = self.findChild(QPushButton, "getDataBtn")
        self.save_button = self.findChild(QPushButton, "saveButton")
        self.reload_button = self.findChild(QPushButton, "reloadButton")

        self.details_box = self.findChild(QGroupBox, "detailsBox")

        self.line_edit_api_key = self.findChild(QLineEdit, "lineEditApiKey")

        self.tab_widget = self.findChild(QTabWidget, "tabWidget")

        self.tab_widget.setCurrentIndex(0)
        self.line_edit_api_key.setText(owmAPI.read_config('API_KEY'))

        self.radios_time = [self.findChild(QRadioButton, "radioButton1"),
                            self.findChild(QRadioButton, "radioButton2"),
                            self.findChild(QRadioButton, "radioButton3")]

        self.radios_unit = [self.findChild(QRadioButton, "radioButtonImperial"),
                            self.findChild(QRadioButton, "radioButtonMetric")]

        self.set_radio()

        self.get_data_btn.clicked.connect(self.set_data)
        self.save_button.clicked.connect(lambda: owmAPI.save_config(
            self.line_edit_api_key.text(),
            self.check_refresh_radio(),
            self.check_unit_radio()))
        self.reload_button.clicked.connect(lambda: reload())

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

    def set_radio(self):
        for i in self.radios_time:
            if i.text() == owmAPI.read_config("REFRESH_TIME"):
                i.setChecked(True)
        for i in self.radios_unit:
            if i.text() == owmAPI.read_config("UNITS"):
                i.setChecked(True)

    def check_refresh_radio(self):
        selected_radio = 0
        for i in self.radios_time:
            if i.isChecked():
                selected_radio = int(i.text())
                print(i.text())
        return selected_radio

    def check_unit_radio(self):
        selected_radio = ''
        for i in self.radios_unit:
            if i.isChecked():
                selected_radio = i.text()
                print(i.text())
        return selected_radio


app = QApplication(sys.argv)
window = WeatherApp()
window.show()
# TODO: something to reload keys for api after save, like refresh time

timer = QTimer()

if owmAPI.check_config_file(window):
    QTimer.singleShot(1, lambda: window.set_data())

    timer.timeout.connect(lambda: window.set_data())
    timer.setInterval(int(owmAPI.read_config("refresh_time")) * 1000)
    timer.start()


def reload():
    print("reload")
    timer.stop()
    print(owmAPI.read_config("refresh_time"))
    timer.setInterval(int(owmAPI.read_config("refresh_time")) * 1000)
    print("after reload")
    print(owmAPI.read_config("refresh_time"))
    timer.start()
    pass


sys.exit(app.exec_())

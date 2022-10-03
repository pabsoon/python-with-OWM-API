import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic

import functions


class WeatherApp(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("WeatherAppGui.ui", self)

        self.setFixedSize(330, 200)

        self.image_label = self.findChild(QLabel, "imageLabel")
        self.temp_label = self.findChild(QLabel, "tempLabel")
        self.description_label = self.findChild(QLabel, "descriptionLabel")
        self.feels_like_label = self.findChild(QLabel, "feelsLikeLabel")
        self.pressure_label = self.findChild(QLabel, "pressureLabel")
        self.humidity_label = self.findChild(QLabel, "humidityLabel")
        self.wind_label = self.findChild(QLabel, "windLabel")
        self.clouds_label = self.findChild(QLabel, "cloudsLabel")

        self.save_button = self.findChild(QPushButton, "saveButton")

        self.details_box = self.findChild(QGroupBox, "detailsBox")

        self.line_edit_api_key = self.findChild(QLineEdit, "lineEditApiKey")

        self.tab_widget = self.findChild(QTabWidget, "tabWidget")

        self.tab_widget.setCurrentIndex(0)
        self.line_edit_api_key.setText(functions.read_config('API_KEY'))

        self.radios_time = [self.findChild(QRadioButton, "radioButton1"),
                            self.findChild(QRadioButton, "radioButton2"),
                            self.findChild(QRadioButton, "radioButton3")]

        self.radios_unit = [self.findChild(QRadioButton, "radioButtonImperial"),
                            self.findChild(QRadioButton, "radioButtonMetric")]

        self.set_radio()

        self.save_button.clicked.connect(
            lambda: functions.save_config(
                self,
                self.line_edit_api_key.text(),
                self.check_refresh_radio(),
                self.check_unit_radio()))

        self.qtimer = QTimer()
        self.qtimer.timeout.connect(lambda: window.set_data())

        QTimer.singleShot(1, lambda: window.set_data())

    def set_data(self):
        data = functions.get_weather_by_city_name(self, "Warsaw", "PL")
        if data != False:
            units = '', ''
            if functions.read_config('UNITS') == 'metric':
                units = '°C', 'm/s'
            else:
                units = '°F', 'm/h'
            image = functions.get_weather_image(data["weather"][0]["icon"])
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
            if i.text() == functions.read_config("REFRESH_TIME"):
                i.setChecked(True)
        for i in self.radios_unit:
            if i.text() == functions.read_config("UNITS"):
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

    def reload_timer(self):
        self.qtimer.stop()
        QTimer.singleShot(1, lambda: window.set_data())
        self.qtimer.setInterval(int(functions.read_config("REFRESH_TIME")) * 1000)
        self.qtimer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    window.reload_timer()
    sys.exit(app.exec_())

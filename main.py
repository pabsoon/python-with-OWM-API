import sys

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic
import owmAPI


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("WeatherAppGui.ui", self)

        self.get_data_btn = self.findChild(QPushButton, "getDataBtn")
        self.plain_text = self.findChild(QPlainTextEdit, "plainText")
        self.image_label = self.findChild(QLabel, "imageLabel")
        self.temp_label = self.findChild(QLabel, "tempLabel")

        self.get_data_btn.clicked.connect(self.get_data)

    def get_data(self):
        weather_response = owmAPI.get_weather_by_city_name(self, "Warsaw", "PL", "metric")
        weather_json = weather_response.json()
        code = weather_json["weather"][0]["icon"]
        image = owmAPI.get_weather_image(self, code)
        temperature = weather_json["main"]["temp"]

        self.plain_text.setPlainText(weather_response.text)
        self.image_label.setPixmap(QPixmap(image))
        self.temp_label.setText(f"{temperature}°")
        pass


app = QApplication(sys.argv)

window = WeatherApp()
window.show()
app.exec_()

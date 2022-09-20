import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
import owmAPI


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("WeatherAppGui.ui", self)

        self.get_data_btn = self.findChild(QPushButton, "getDataBtn")
        self.plain_text = self.findChild(QPlainTextEdit, "plainText")

        self.get_data_btn.clicked.connect(self.get_data)

    def get_data(self):
        response = owmAPI.get_weather_by_city_name(self, "Warsaw", "PL", "metric")
        output = ""
        if response.status_code == 200:
            output = response.text
        else:
            output = f"Error due to download data. Status code: {response.status_code}"
        self.plain_text.setPlainText(output)
        pass


app = QApplication(sys.argv)

window = WeatherApp()
window.show()
app.exec_()

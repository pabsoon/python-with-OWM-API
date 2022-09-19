import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("WeatherAppGui.ui", self)
        window_width = 300
        window_height = 200
        self.setFixedSize(window_width, window_height)

        self.temp_label = self.findChild(QLabel, "temperature")
        self.image_label = self.findChild(QGraphicsView, "image")


app = QApplication(sys.argv)

window = WeatherApp()
window.show()
app.exec_()

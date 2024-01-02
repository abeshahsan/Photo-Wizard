from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths
import json
import copy
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UI_FilterInputDialog(QDialog):
    def __init__(self):
        super(UI_FilterInputDialog, self).__init__()
        uic.loadUi(Filepaths.FILTER_INPUT_DIALOG(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.save_button = self.findChild(QWidget, "save_button")

        """Get values from the Dialog"""

        self.filter_name = self.findChild(QLineEdit, "filter_name")
        self.brightness = self.findChild(QLineEdit, "brightness")
        self.saturation = self.findChild(QLineEdit, "saturation")
        self.contrast = self.findChild(QLineEdit, "contrast")
        self.warmth = self.findChild(QLineEdit, "warmth")
        self.exposure = self.findChild(QLineEdit, "exposure")


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_FilterInputDialog()
    widget.show()
    app.exec()

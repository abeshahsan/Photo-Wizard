from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths


class UI_EditToolbarWidget(QWidget):
    def __init__(self):
        super(UI_EditToolbarWidget, self).__init__()
        uic.loadUi(Filepaths.EDIT_TOOLBAR(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.crop_button = self.findChild(QPushButton, "crop_button")
        self.adjustment_button = self.findChild(QPushButton, "adjustment_button")
        self.filter_button = self.findChild(QPushButton, "filter_button")
        self.doodle_button = self.findChild(QPushButton, "doodle_button")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")

        self.crop_button.setFixedWidth(50)
        self.adjustment_button.setFixedWidth(50)
        self.filter_button.setFixedWidth(50)
        self.doodle_button.setFixedWidth(50)
        self.cancel_button.setFixedWidth(50)


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_EditToolbarWidget()
    widget.show()
    app.exec()

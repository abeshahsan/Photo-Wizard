from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths


class UI_ViewToolbarWidget(QWidget):
    def __init__(self):
        super(UI_ViewToolbarWidget, self).__init__()
        uic.loadUi(Filepaths.VIEW_TOOLBAR(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.edit_button = self.findChild(QWidget, "edit_button")
        self.rotate_button = self.findChild(QWidget, "rotate_button")

        self.edit_button.setFixedWidth(50)
        self.rotate_button.setFixedWidth(50)


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_ViewToolbarWidget()
    widget.show()
    app.exec()

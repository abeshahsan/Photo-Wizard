from PyQt6 import uic
from PyQt6.QtWidgets import *

from filepaths import Filepaths


class UI_AdjustWidget(QWidget):
    def __init__(self):
        super(UI_AdjustWidget, self).__init__()
        uic.loadUi(Filepaths.ADJUST_WIDGET(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_AdjustWidget()
    widget.show()
    app.exec()

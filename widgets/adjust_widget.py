from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from filepaths import Filepaths
from utilites import ValueProperty, pixmap_to_numpy, numpy_to_pixmap
from widgets.crop_rubberband_widget import CropRubberBandWidget


class UI_AdjustWidget(QWidget):
    def __init__(self, parent):
        super(UI_AdjustWidget, self).__init__(parent)
        uic.loadUi(Filepaths.ADJUST_WIDGET(), self)


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_AdjustWidget()
    widget.show()
    app.exec()

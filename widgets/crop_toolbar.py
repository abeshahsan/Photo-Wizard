from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths


class UI_CropToolbarWidget(QWidget):
    def __init__(self):
        super(UI_CropToolbarWidget, self).__init__()
        uic.loadUi(Filepaths.CROP_TOOLBAR(), self)

        self.cancel_button = self.findChild(QPushButton, "cancel_button")
        self.save_button = self.findChild(QPushButton, "save_button")
        self.mirror_lr_button = self.findChild(QPushButton, "mirror_lr_button")
        self.mirror_ud_button = self.findChild(QPushButton, "mirror_ud_button")
        self.rotate_button = self.findChild(QPushButton, "rotate_button")

       
        self.cancel_button.setFixedWidth(80)
        self.save_button.setFixedWidth(80)
        self.mirror_lr_button.setFixedWidth(80)
        self.mirror_ud_button.setFixedWidth(80)
        self.rotate_button.setFixedWidth(80)


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_CropToolbarWidget()
    widget.show()
    app.exec()

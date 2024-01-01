from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths


class UI_AdjustWidget(QWidget):
    def __init__(self, canvas_controller):
        super(UI_AdjustWidget, self).__init__()
        uic.loadUi(Filepaths.ADJUST_WIDGET(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")

        # print(self.main_widget)

        self.blur_slider = self.findChild(QWidget, "blur_slider")
        self.sharpen_slider = self.findChild(QWidget, "sharpen_slider")
        self.canvas_controller = canvas_controller

        self.blur_slider.valueChanged.connect(self.blur)
        self.sharpen_slider.valueChanged.connect(self.sharpen)

    def blur(self):
        self.canvas_controller.scene_image = image_operations.blur(self.canvas_controller.original_image)
        self.canvas_controller.scene_image_updated.value = True

    def sharpen(self):
        self.canvas_controller.scene_image = image_operations.sharpen(self.canvas_controller.original_image)
        self.canvas_controller.scene_image_updated.value = True


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_AdjustWidget()
    widget.show()
    app.exec()

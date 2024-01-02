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

        self.blur_slider = self.findChild(QSlider, "blur_slider")
        self.sharpen_slider = self.findChild(QSlider, "sharpen_slider")
        self.contrast_slider = self.findChild(QSlider, "contrast_slider")
        self.brightness_slider = self.findChild(QSlider, "brightness_slider")
        self.exposure_slider = self.findChild(QSlider, "exposure_slider")
        self.warmth_slider = self.findChild(QSlider, "warmth_slider")
        self.saturation_slider = self.findChild(QSlider, "saturation_slider")
        self.canvas_controller = canvas_controller

        self.blur_slider.valueChanged.connect(self.blur)
        self.sharpen_slider.valueChanged.connect(self.sharpen)
        self.contrast_slider.valueChanged.connect(self.contrast)
        self.brightness_slider.valueChanged.connect(self.brightness)
        self.saturation_slider.valueChanged.connect(self.saturation)
        self.warmth_slider.valueChanged.connect(self.warmth)
        self.exposure_slider.valueChanged.connect(self.exposure)

    def blur(self):
        self.canvas_controller.scene_image = image_operations.blur(self.canvas_controller.original_image)
        self.canvas_controller.scene_image_updated.value = True

    def sharpen(self):
        self.canvas_controller.scene_image = image_operations.sharpen(self.canvas_controller.original_image)
        self.canvas_controller.scene_image_updated.value = True

    def contrast(self):
        self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.original_image,
                                                                              self.contrast_slider.value() / 10.0)

        print(self.contrast_slider.value())
        self.canvas_controller.scene_image_updated.value = True

    def brightness(self):
        self.canvas_controller.scene_image = image_operations.change_brightness(self.canvas_controller.original_image,
                                                                                self.brightness_slider.value())
        self.canvas_controller.scene_image_updated.value = True

    def warmth(self):
        self.canvas_controller.scene_image = image_operations.change_warmth(self.canvas_controller.original_image,
                                                                            self.warmth_slider.value())
        self.canvas_controller.scene_image_updated.value = True

    def saturation(self):
        self.canvas_controller.scene_image = image_operations.change_saturation(self.canvas_controller.original_image,
                                                                                self.saturation_slider.value() / 10.0)
        self.canvas_controller.scene_image_updated.value = True

    def exposure(self):
        self.canvas_controller.scene_image = image_operations.change_exposure(self.canvas_controller.original_image,
                                                                              self.exposure_slider.value() / 10.0)
        self.canvas_controller.scene_image_updated.value = True


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_AdjustWidget()
    widget.show()
    app.exec()

from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from canvas_controller import CanvasController
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
        contrast_factor = ((self.contrast_slider.value() - self.contrast_slider.minimum()) / (
                self.contrast_slider.maximum() - self.contrast_slider.minimum())) * 1.2 + 1.0
        self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.original_image,
                                                                              contrast_factor)

        print(self.contrast_slider.value())
        self.canvas_controller.scene_image_updated.value = True

    def brightness(self):
        brightness_factor = ((self.brightness_slider.value() - self.brightness_slider.minimum()) / (
                self.brightness_slider.maximum() - self.brightness_slider.minimum())) * 20.0 + 0.0
        self.canvas_controller.scene_image = image_operations.change_brightness(self.canvas_controller.original_image,
                                                                                brightness_factor)
        self.canvas_controller.scene_image_updated.value = True

    def warmth(self):
        warmth_factor = ((self.warmth_slider.value() - self.warmth_slider.minimum()) / (
                self.warmth_slider.maximum() - self.warmth_slider.minimum())) * 0.2 + 1.0
        self.canvas_controller.scene_image = image_operations.change_warmth(self.canvas_controller.original_image,
                                                                            warmth_factor)
        self.canvas_controller.scene_image_updated.value = True

    def saturation(self):
        saturation_factor = ((self.saturation_slider.value() - self.saturation_slider.minimum()) / (
                self.saturation_slider.maximum() - self.saturation_slider.minimum())) * 0.4 + 1.0
        self.canvas_controller.scene_image = image_operations.change_saturation(self.canvas_controller.original_image,
                                                                                saturation_factor)
        self.canvas_controller.scene_image_updated.value = True

    def exposure(self):
        exposure_factor = ((self.exposure_slider.value() - self.exposure_slider.minimum()) / (
                self.exposure_slider.maximum() - self.exposure_slider.minimum())) * 0.8 + 1.0
        self.canvas_controller.scene_image = image_operations.change_exposure(self.canvas_controller.original_image,
                                                                              self.exposure_slider.value() / 10.0)
        self.canvas_controller.scene_image_updated.value = True


if __name__ == "__main__":
    canvas_controller = CanvasController()
    app = QApplication([])
    widget = UI_AdjustWidget(canvas_controller)
    widget.show()
    app.exec()

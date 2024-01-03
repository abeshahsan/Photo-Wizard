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

from widgets.filter_input_dialog import UI_FilterInputDialog


class UI_FilterWidget(QWidget):
    def __init__(self, canvas_controller):
        super(UI_FilterWidget, self).__init__()
        uic.loadUi(Filepaths.FILTER_WIDGET(), self)

        self.filters = None

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.filter_area = self.findChild(QScrollArea, "scrollArea")
        self.add_new_filter_button = self.findChild(QPushButton, "add_new_filter_button")
        self.add_new_filter_button.clicked.connect(self.open_filter_input_dialog)
        self.read_filters(Filepaths.FILTER_FILE())
        self.canvas_controller = canvas_controller

        self.add_filter_buttons()

        self.filter_input_dialog = None

    def event_clicked_on_vintage(self):
        sender_button = self.sender()
        button_name = sender_button.objectName()
        print(f"The button '{button_name}' was clicked.")
        self.apply_filter(button_name)

    def apply_filter(self, filter_name):
        try:
            self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.original_image,
                                                                                  self.filters[filter_name]["Contrast"])
            self.canvas_controller.scene_image = image_operations.change_exposure(self.canvas_controller.scene_image,
                                                                                  self.filters[filter_name]["Exposure"])
            self.canvas_controller.scene_image = image_operations.change_warmth(self.canvas_controller.scene_image,
                                                                                self.filters[filter_name]["Warmth"])
            self.canvas_controller.scene_image = image_operations.change_brightness(self.canvas_controller.scene_image,
                                                                                    self.filters[filter_name][
                                                                                        "Brightness"])
            self.canvas_controller.scene_image = image_operations.change_saturation(self.canvas_controller.scene_image,
                                                                                    self.filters[filter_name][
                                                                                        "Saturation"])
            self.canvas_controller.scene_image_updated.value = True
        except Exception as e:
            print(e)

    def write_filters(self, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(self.filters, json_file, indent=4)
        print(f"Vintage filter parameters saved to {file_path}")

    def read_filters(self, file_path):
        with open(file_path, 'r') as json_file:
            self.filters = json.load(json_file)

    def add_filter_button(self, filter_name):
        button = QPushButton(filter_name)
        button.setObjectName(filter_name)
        button.setFixedWidth(120)
        button.setFixedHeight(50)
        button.clicked.connect(self.event_clicked_on_vintage)
        self.filter_area.widget().layout().insertWidget(len(self.filter_area.widget().layout()) - 2, button)
    
    def add_filter_buttons(self):
        for filter_name in self.filters.keys():
            self.add_filter_button(filter_name)

    def open_filter_input_dialog(self):
        self.filter_input_dialog = UI_FilterInputDialog()
        self.filter_input_dialog.save_button.clicked.connect(self.event_click_save_button)
        self.filter_input_dialog.show()

    def event_click_save_button(self):
        
        saturation_value = 1.0
        contrast_value = 1.0
        brightness_value = 0.0
        exposure_value = 1.0
        warmth_value = 1.0
        
        try:    
            saturation_value = float(self.filter_input_dialog.saturation.text())
            if saturation_value < 0.6 or saturation_value > 1.4:
                raise Exception("Invalid saturation value")
            contrast_value = float(self.filter_input_dialog.contrast.text())
            if contrast_value < 0.6 or contrast_value > 1.4:
                raise Exception("Invalid contrast value")
            brightness_value = float(self.filter_input_dialog.brightness.text())
            if brightness_value < -100 or brightness_value > 100:
                raise Exception("Invalid brightness value")
            exposure_value = float(self.filter_input_dialog.exposure.text())
            if exposure_value < 0.6 or exposure_value > 1.4:
                raise Exception("Invalid exposure value")
            warmth_value = float(self.filter_input_dialog.warmth.text())
            if warmth_value < 0.6 or warmth_value > 1.4:
                raise Exception("Invalid warmth value")
        
        except Exception as e:
            print("error processing input dialog message " + str(e))
            self.filter_input_dialog.error_label.setText("Ivalid input")
            return
        
        self.filters[self.filter_input_dialog.filter_name.text()] = {
            "Saturation": saturation_value,
            "Contrast": contrast_value,
            "Brightness": brightness_value,
            "Exposure": exposure_value,
            "Warmth": warmth_value
        }
        
        self.add_filter_button(self.filter_input_dialog.filter_name.text())
        
        self.write_filters(Filepaths.FILTER_FILE())

        self.filter_input_dialog.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_FilterWidget(None)
    widget.show()
    app.exec()

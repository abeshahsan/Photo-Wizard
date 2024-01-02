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


class UI_FilterWidget(QWidget):
    def __init__(self, canvas_controller):
        super(UI_FilterWidget, self).__init__()
        uic.loadUi(Filepaths.FILTER_WIDGET(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.vintage_filter = self.findChild(QPushButton, "vintage")
        self.filters = self.read_filters(Filepaths.FILTER_FILE())
        self.canvas_controller = canvas_controller

        self.vintage_filter.clicked.connect(self.event_clicked_on_vintage)

    def event_clicked_on_vintage(self):
        sender_button = self.sender()
        button_name = sender_button.objectName()
        print(f"The button '{button_name}' was clicked.")
        self.apply_filter("")

    def apply_filter(self, filter_name):
        try:
            self.canvas_controller.scene_image = image_operations.change_exposure(self.canvas_controller.scene_image, 2.0)
            
            # self.canvas_controller.scene_image = image_operations.change_saturation(self.canvas_controller.scene_image, self.filters["vintage"]["saturation"])
            # self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.scene_image, self.filters["vintage"]["contrast"])
            
            # self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.scene_image, 1.2)
            
            # print("Crashed 2")
            # self.canvas_controller.scene_image = image_operations.change_warmth(self.canvas_controller.scene_image, self.filters["vintage"]["warmth"])
            self.canvas_controller.scene_image_updated.value = True
        except Exception as e:
            print(e)

    def write_filters(self, file_path, params):
        with open(file_path, 'w') as json_file:
            json.dump(params, json_file, indent=4)
        print(f"Vintage filter parameters saved to {file_path}")

    def read_filters(self, file_path):
        with open(file_path, 'r') as json_file:
            params = json.load(json_file)
        return params
    


if __name__ == "__main__":
    app = QApplication([])
    widget = UI_FilterWidget()
    widget.show()
    app.exec()

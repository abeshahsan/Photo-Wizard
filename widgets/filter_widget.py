from PyQt6 import uic
from PyQt6.QtWidgets import *

import image_operations
from filepaths import Filepaths
import json


class UI_FilterWidget(QWidget):
    def __init__(self, canvas_controller):
        super(UI_FilterWidget, self).__init__()
        uic.loadUi(Filepaths.FILTER_WIDGET(), self)

        self.main_widget = self.findChild(QWidget, "main_widget")
        self.vintage_filter = self.findChild(QPushButton, "vintage")
        self.filters = self.read_filters(Filepaths.FILTER_FILE())

        self.vintage_filter.clicked.connect(self.event_clicked_on_vintage)

    def event_clicked_on_vintage(self):
        sender_button = self.sender()
        button_name = sender_button.objectName()
        print(f"The button '{button_name}' was clicked.")

    def apply_filter(self, filter_name):
        self.canvas_controller.scene_image = image_operations.change_saturation(self.canvas_controller.scene_image)
        self.canvas_controller.scene_image = image_operations.change_contrast(self.canvas_controller.scene_image)
        self.canvas_controller.scene_image = image_operations.change_exposure(self.canvas_controller.scene_image)
        self.canvas_controller.scene_image = image_operations.change_warmth(self.canvas_controller.scene_image)
        self.canvas_controller.scene_image_updated.value = True

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

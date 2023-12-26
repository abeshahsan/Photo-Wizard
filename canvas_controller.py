import sys

import numpy as np
from PyQt6.QtGui import QImage, QPixmap

import copy

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene
import image_operations

from utilites import ValueProperty


class CanvasController:
    def __init__(self):
        self.original_image = QImage()
        self.scene_image = QImage()
        self.numpy_array = None
        self.scene_image_updated = ValueProperty(False)

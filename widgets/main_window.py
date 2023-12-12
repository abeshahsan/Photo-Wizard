import sys

from copy import deepcopy
import numpy as np
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from filepaths import Filepaths
from utilites import ValueProperty


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.save_file_path = None
        uic.loadUi(Filepaths.MAIN_WINDOW(), self)
        self.setWindowTitle('Photo Wizard')
        # self.setFixedSize(800, 600)

        self.canvas = self.findChild(QGraphicsView, 'canvas')
        self.v_layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.pixmap = None

        self.canvas_empty = ValueProperty(True)
        self.canvas_empty.valueChanged.connect(self.enable_all)
        self.action_open.triggered.connect(self.open_image)
        self.action_save_as.triggered.connect(self.save_new_file)
        self.action_save.triggered.connect(self.save_file)

        self.rubber_band = CropRubberBandWidget(parent=self.canvas)
        self.rubber_band.setGeometry(0, 0, 80, 80)

        self.rubber_band.show()

    def choose_file(self):
        file_dialogue = QFileDialog(self)
        filters = "Images (*.jpg *.png *.bmp)"
        filenames, _ = file_dialogue.getOpenFileNames(self, filter=filters)
        if not filenames:
            return
        return filenames[0]

    def open_image(self):
        image_file_path = self.choose_file()

        self.pixmap = QPixmap(image_file_path)
        if not self.pixmap.isNull():
            if self.pixmap.width() >= self.canvas.width() or self.pixmap.height() >= self.canvas.height():
                self.pixmap = self.pixmap.scaled(int(self.canvas.width() * .99), int(self.canvas.height() * .99),
                                                 Qt.AspectRatioMode.KeepAspectRatio)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(self.pixmap)
            self.canvas.setScene(self.scene)
            self.enable_all()

    def enable_all(self):
        self.action_save_as.setEnabled(True)
        self.action_save.setEnabled(True)
        # self.blur_select_button.setEnabled(True)
        # self.rotate_button.setEnabled(True)

    def save_new_file(self):
        file_dialogue = QFileDialog()
        filters = "Images (*.jpg *.png *.bmp)"
        file_path, _ = file_dialogue.getSaveFileName(filter=filters)
        self.save_file_path = file_path
        if file_path:
            self.pixmap.save(file_path)

    def save_file(self):
        if self.save_file_path:
            self.pixmap.save(self.save_file_path)
        else:
            self.save_new_file()


class CropRubberBandWidget(QWidget):
    def __init__(self, parent=None):
        super(CropRubberBandWidget, self).__init__(parent=parent)
        self.setWindowFlag(Qt.WindowType.SubWindow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.rubber_band.setPalette(QPalette(Qt.GlobalColor.red))

        self.mouse_event_previous_pos = None
        self.mouse_event_new_pos = None

    def mousePressEvent(self, event):
        self.mouse_event_previous_pos = QCursor.pos()

    def mouseReleaseEvent(self, event):
        self.mouse_event_previous_pos = self.mouse_event_new_pos
        self.mouse_event_new_pos = QCursor.pos()

    def resizeEvent(self, event):
        self.rubber_band.resize(self.width(), self.height())

    def mouseMoveEvent(self, event):
        if self.mouse_event_previous_pos:
            diff = QCursor.pos() - self.mouse_event_previous_pos
            self.move(self.pos() + diff)
            self.mouse_event_previous_pos = QCursor.pos()

    def show(self):
        self.rubber_band.show()
        super().show()


if __name__ == "__main__":
    app = QApplication([])
    widget = CropRubberBandWidget()
    widget.show()
    app.exec()

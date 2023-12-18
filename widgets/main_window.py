import copy

from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from filepaths import Filepaths
from utilites import ValueProperty, pixmap_to_numpy, numpy_to_pixmap
from widgets.crop_rubberband_widget import CropRubberBandWidget
from widgets.adjust_widget import UI_AdjustWidget
import image_operations


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Filepaths.MAIN_WINDOW(), self)
        self.setWindowTitle('Photo Wizard')
        # self.setFixedSize(800, 600)

        """Loading necessary objects from the loaded ui."""
        # The canvas is to hold the image to be shown on the screen.
        self.canvas = self.findChild(QGraphicsView, 'canvas')
        self.editor_container = self.findChild(QHBoxLayout, 'editor_container')
        self.cancel_button = self.findChild(QPushButton, 'cancel_button')

        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)

        """Some necessary variables needed for canvas. Initializing with None now. will need later."""
        self.adjust_widget = None
        self.save_file_path = None
        self.pixmap = None
        self.original_image = None
        self.scene_image = None
        self.crop_rubber_band = None

        self.load_adjust_widget()

        """Some event handlers needed for different operations."""
        self.action_open.triggered.connect(self.open_image)
        self.action_save_as.triggered.connect(self.save_new_file)
        self.action_save.triggered.connect(self.save_file)
        # self.cancel_button.clicked.connect(self.load_adjust_widget)

    def choose_file(self):
        """
        Opens a file dialog. lets the user choose a file to open and returns the path of the file.
        :return: the path of the selected file.
        """
        file_dialogue = QFileDialog(self)
        filters = "Images (*.jpg *.png *.bmp)"
        filenames, _ = file_dialogue.getOpenFileNames(self, filter=filters)
        if not filenames:
            return
        return filenames[0]

    def open_image(self):
        """
        Clicking 'Open' or pressing Ctrl+O \n
        Opens an image file and loads it into the screen.\n
        * Opens a file dialog. Using the choose_file() method.
        * If you select an image file, it loads it into the screen.
        :return:
        """
        image_file_path = self.choose_file()

        self.pixmap = QPixmap(image_file_path)
        self.original_image = self.pixmap.toImage().copy()
        self.scene_image = self.original_image.copy()
        if self.pixmap is not None and not self.pixmap.isNull():
            self.scale_pixmap()
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
        """
        Clicking 'Save as' or pressing Ctrl+Shift+S \n
        If you want to save the image file for the first time, you need to create a file. \n
        So a file-dialogue will open to get the directory and the filename.
        :return:
        """
        file_dialogue = QFileDialog(self)
        filters = "Images (*.jpg *.png *.bmp)"
        file_path, _ = file_dialogue.getSaveFileName(filter=filters, parent=self)
        self.save_file_path = file_path
        if file_path:
            self.pixmap.save(file_path)

    def save_file(self):
        """
        Clicking 'Save' or pressing Ctrl+S \n
        Save the file, when the save-file already exists/created,
        :return:
        """
        if self.save_file_path:
            self.pixmap.save(self.save_file_path)
        else:  # If the save-file is not created, call save_new_file()
            self.save_new_file()

    def scale_pixmap(self):
        """
        If the original image is bigger than the canvas, scale it down to fit. \n
        But if it is smaller or equal, keep it as it is.
        :return:
        """
        if self.pixmap.width() >= self.canvas.width() or self.pixmap.height() >= self.canvas.height():
            self.pixmap = self.pixmap.scaled(int(self.canvas.width() * .99), int(self.canvas.height() * .99),
                                             Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)

    def crop_pixmap(self):
        numpy_array = pixmap_to_numpy(self.pixmap)
        top, right, bottom, left = self.rubber_band.get_crop_dimensions()
        numpy_array = numpy_array[top:bottom, left:right]
        self.pixmap = numpy_to_pixmap(numpy_array)
        return self.pixmap

    def update_scene(self):
        self.pixmap = QPixmap(self.scene_image)
        self.scale_pixmap()
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.canvas.setScene(self.scene)

    def load_adjust_widget(self):
        if self.adjust_widget is None:
            self.adjust_widget = UI_AdjustWidget()
            self.editor_container.addWidget(self.adjust_widget.main_widget)
            self.editor_container.setStretch(0, 1)

    def load_crop_rubberband(self):
        self.crop_rubber_band = CropRubberBandWidget(self.canvas)
        self.crop_rubber_band.setGeometry(0, 0, self.width(), self.height())
        self.crop_rubber_band.show()

    def blur(self):
        self.scene_image = image_operations.blur_image(self.original_image)
        self.update_scene()


if __name__ == "__main__":
    app = QApplication([])
    widget = CropRubberBandWidget()
    widget.show()
    app.exec()

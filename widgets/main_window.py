from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from filepaths import Filepaths
from utilites import ValueProperty, pixmap_to_numpy, numpy_to_pixmap
from widgets.crop_rubberband_widget import CropRubberBandWidget


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.save_file_path = None
        uic.loadUi(Filepaths.MAIN_WINDOW(), self)
        self.setWindowTitle('Photo Wizard')
        # self.setFixedSize(800, 600)

        self.canvas = self.findChild(QGraphicsView, 'canvas')
        self.crop_button = self.findChild(QPushButton, 'pushButton')

        self.crop_button.clicked.connect(self.update_scene)

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

    def resizeEvent(self, event):
        self.canvas.setFixedWidth(int(self.centralWidget().width() * 0.98))
        self.canvas.setFixedHeight(int(self.centralWidget().height() * 0.98))

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
        if self.pixmap is not None and not self.pixmap.isNull():
            self.scale_pixmap()
            self.scene = QGraphicsScene()
            self.scene.addPixmap(self.pixmap)
            self.canvas.setScene(self.scene)
            array = pixmap_to_numpy(self.pixmap)
            print(array.shape)
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

    def scale_pixmap(self):
        if self.pixmap.width() >= self.canvas.width() or self.pixmap.height() >= self.canvas.height():
            self.pixmap = self.pixmap.scaled(int(self.canvas.width() * .99), int(self.canvas.height() * .99),
                                             Qt.AspectRatioMode.KeepAspectRatio)

    def crop_pixmap(self):
        numpy_array = pixmap_to_numpy(self.pixmap)
        top, right, bottom, left = self.rubber_band.get_crop_dimensions()
        numpy_array = numpy_array[top:bottom, left:right]
        self.pixmap = numpy_to_pixmap(numpy_array)
        return self.pixmap

    def update_scene(self):
        self.pixmap = self.crop_pixmap()
        self.scale_pixmap()
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.canvas.setScene(self.scene)


if __name__ == "__main__":
    app = QApplication([])
    widget = CropRubberBandWidget()
    widget.show()
    app.exec()

from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import image_operations
from canvas_controller import CanvasController
from filepaths import Filepaths
from widgets.adjust_widget import UI_AdjustWidget
from widgets.crop_rubberband_widget import CropRubberBandWidget
from widgets.edit_toolbar import UI_EditToolbarWidget
from widgets.view_toolbar import UI_ViewToolbarWidget
from widgets.filter_widget import UI_FilterWidget


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Filepaths.MAIN_WINDOW(), self)
        self.setWindowTitle('Photo Wizard')

        """Loading necessary objects from the loaded ui."""
        # The canvas is to hold the image to be shown on the screen.
        self.canvas = self.findChild(QGraphicsView, 'canvas')
        self.editor_container = self.findChild(QHBoxLayout, 'editor_container')
        self.horizontalLayout_3 = self.findChild(QHBoxLayout, 'horizontalLayout_3')
        self.cancel_button = self.findChild(QPushButton, 'cancel_button')
        self.toolbar = self.findChild(QHBoxLayout, 'toolbar')

        """Some necessary variables needed for canvas. Initializing with None now. will need later."""
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.adjust_widget = None
        self.filter_widget = None
        self.save_file_path = None
        self.scene_pixmap = None
        self.original_pixmap = None
        self.crop_rubber_band = None
        self.view_toolbar_edit_button = None
        self.view_toolbar_rotate_button = None

        """create a CanvasController to store all the elements related to the canvas."""
        self.canvas_controller = CanvasController()

        """Load the necessary widgets. This will just load the UI file, but will not add it to the scene yet."""
        self.adjust_widget = UI_AdjustWidget(self.canvas_controller)
        self.view_toolbar_widget = UI_ViewToolbarWidget()
        self.edit_toolbar_widget = UI_EditToolbarWidget()
        self.filter_widget = UI_FilterWidget(self.canvas_controller)

        """Some event handlers needed for different operations."""
        self.action_open.triggered.connect(self.open_image)
        self.action_save_as.triggered.connect(self.save_new_file)
        self.action_save.triggered.connect(self.save_file)
        self.canvas_controller.scene_image_updated.valueChanged.connect(self.update_canvas)
        self.view_toolbar_widget.edit_button.clicked.connect(self.event_clicked_on_edit_button)
        self.edit_toolbar_widget.adjustment_button.clicked.connect(self.event_clicked_on_adjustment_button)
        self.edit_toolbar_widget.cancel_button.clicked.connect(self.event_clicked_on_cancel_button)
        self.edit_toolbar_widget.crop_button.clicked.connect(self.event_clicked_on_crop_button)
        self.edit_toolbar_widget.save_button.clicked.connect(self.save_button_clicked_on_edit_toolbar)
        self.edit_toolbar_widget.filter_button.clicked.connect(self.event_clicked_on_filter_button)
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
        self.add_view_toolbar_widget()
        image_file_path = self.choose_file()
        self.enable_all()
        
        self.original_pixmap = QPixmap(image_file_path)
        self.scene_pixmap = self.original_pixmap.copy()
        self.canvas_controller.original_image = self.scene_pixmap.toImage().copy()
        self.canvas_controller.scene_image = self.canvas_controller.original_image.copy()
        if self.scene_pixmap is not None and not self.scene_pixmap.isNull():
            self.update_canvas()

    def enable_all(self):
        self.action_save_as.setEnabled(True)
        self.action_save.setEnabled(True)
        # self.blur_select_button.setEnabled(True)
        # self.rotate_button.setEnabled(True)

    def save_new_file(self):
        """
        Clicking 'Save as' or pressing Ctrl+Shift+S. \n
        If you want to save the image file for the first time, you need to create a file. \n
        So a file-dialogue will open to get the directory and the filename.
        :return:
        """
        file_dialogue = QFileDialog(self)
        filters = "Images (*.jpg *.png *.bmp)"
        file_path, _ = file_dialogue.getSaveFileName(filter=filters, parent=self)
        self.save_file_path = file_path
        if file_path:
            self.scene_pixmap.save(file_path)

    def save_file(self):
        """
        Clicking 'Save' or pressing Ctrl+S. \n
        Save the file, when the save-file already exists/created,
        :return:
        """
        if self.save_file_path:
            self.scene_pixmap.save(self.save_file_path)
        else:  # If the save-file is not created, call save_new_file()
            self.save_new_file()

    def scale_pixmap(self):
        """
        If the original image is bigger than the canvas, scale it down to fit. \n
        But if it is smaller or equal, keep it as it is.
        :return:
        """
        if self.original_pixmap.width() >= self.canvas.width() or self.original_pixmap.height() >= self.canvas.height():
            self.scene_pixmap = self.original_pixmap.scaled(int(self.canvas.width() * .99),
                                                            int(self.canvas.height() * .99),
                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                            Qt.TransformationMode.SmoothTransformation)
        else:
            self.scene_pixmap = self.original_pixmap.copy()

    def update_canvas(self):
        if not self.canvas_controller.scene_image_updated:
            return
        self.original_pixmap = QPixmap(self.canvas_controller.scene_image)
        self.scale_pixmap()
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.scene_pixmap)
        pixmap_item = QGraphicsPixmapItem(self.scene_pixmap)
        print(pixmap_item.scenePos())
        self.canvas.setScene(self.scene)
        self.canvas_controller.scene_image_updated.value = False

    def add_adjust_widget(self):
        self.editor_container.addWidget(self.adjust_widget.main_widget)
        self.editor_container.setStretch(0, 1)

    def remove_adjust_widget(self):
        self.editor_container.removeWidget(self.adjust_widget.main_widget)
        self.adjust_widget.main_widget.setParent(None)
        self.adjust_widget.main_widget.close()

    def add_view_toolbar_widget(self):
        self.toolbar.addWidget(self.view_toolbar_widget.main_widget)

    def remove_view_toolbar_widget(self):
        self.toolbar.removeWidget(self.view_toolbar_widget.main_widget)
        self.view_toolbar_widget.main_widget.setParent(None)
        # self.view_toolbar_widget.main_widget.close()

    def add_crop_rubberband(self):
        self.crop_rubber_band = CropRubberBandWidget(self.canvas)
        self.crop_rubber_band.setGeometry(self.canvas.pos().x(), self.canvas.pos().y(), self.scene_pixmap.width(),
                                          self.scene_pixmap.height())
        self.crop_rubber_band.show()

    def remove_crop_rubberband(self):
        if self.crop_rubber_band:
            self.crop_rubber_band.close()

    def resizeEvent(self, event):
        if self.original_pixmap:
            self.canvas_controller.scene_image_updated.value = True

    def event_clicked_on_edit_button(self):
        # self.add_adjust_widget()
        self.remove_view_toolbar_widget()
        self.add_edit_toolbar_widget()
        self.canvas_controller.scene_image_updated.value = True

    def add_edit_toolbar_widget(self):
        self.toolbar.addWidget(self.edit_toolbar_widget.main_widget)

    def remove_edit_toolbar_widget(self):
        self.toolbar.removeWidget(self.edit_toolbar_widget.main_widget)
        self.edit_toolbar_widget.main_widget.setParent(None)

    def event_clicked_on_adjustment_button(self):
        self.add_adjust_widget()
        self.remove_crop_rubberband()
        self.remove_filter_widget()
        self.canvas_controller.scene_image_updated.value = True

    def event_clicked_on_cancel_button(self):
        self.remove_adjust_widget()
        self.remove_edit_toolbar_widget()
        self.remove_crop_rubberband()
        self.remove_filter_widget()
        self.add_view_toolbar_widget()
        self.canvas_controller.scene_image_updated.value = True

    def event_clicked_on_crop_button(self):
        self.remove_adjust_widget()
        self.remove_filter_widget()
        self.add_crop_rubberband()
        self.canvas_controller.scene_image_updated.value = True

    def save_button_clicked_on_edit_toolbar(self):
        top, bottom, right, left = self.crop_rubber_band.get_crop_dimensions()
        self.canvas_controller.scene_image = image_operations.crop(self.canvas_controller.scene_image, top, bottom, right, left)
        self.canvas_controller.scene_image_updated.value = True

    def add_filter_widget(self):
        self.editor_container.addWidget(self.filter_widget.main_widget)
        self.editor_container.setStretch(0, 1)

    def remove_filter_widget(self):
        self.editor_container.removeWidget(self.filter_widget.main_widget)
        self.filter_widget.main_widget.setParent(None)
        self.filter_widget.main_widget.close()

    def event_clicked_on_filter_button(self):
        self.remove_adjust_widget()
        self.add_filter_widget()
        self.canvas_controller.scene_image_updated.value = True


if __name__ == "__main__":
    app = QApplication([])
    widget = CropRubberBandWidget()
    widget.show()
    app.exec()

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QCursor
from PyQt6.QtWidgets import QHBoxLayout, QSizeGrip, QRubberBand, QWidget


class CropRubberBandWidget(QWidget):
    """
    \n The CropRubberBandWidget class inherits QWidget.
    \n It is used to crop an Image loaded into the QMainWindow.
    \n It contains a rubber-band (QRubberBand), A QHBoxLayout with some QSizeGrip to resize the itself.
    """

    def __init__(self, parent=None, canvas_controller=None):
        # Initialize the super class QWidget
        super(CropRubberBandWidget, self).__init__(parent=parent)
        # Make the Rubberband a sub-window
        self.setWindowFlag(Qt.WindowType.SubWindow)

        self.canvas_controller = canvas_controller

        # Create a layout and make the CropRubberBandWidget as its parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # Add QSizeGrips to the layout, to resize the CropRubberBandWidget
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # Create a Rectangle QRubberBand and make the CropRubberBandWidget as its parent
        self.__rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)

        # To manage the MouseEvents while moving or resizing of the CropRubberBandWidget
        self.mouse_event_previous_pos = None
        self.mouse_event_new_pos = None

        # The 4 min, max values of the 4 sides of the cropping widget
        # They will be used to crop the image
        self.left, self.right, self.top, self.bottom = 0, 0, 0, 0

    def resizeEvent(self, event):
        self.__rubber_band.resize(self.width(), self.height())
        self.update_crop_dimensions()

    def mousePressEvent(self, event):
        self.mouse_event_previous_pos = QCursor.pos()

    def mouseReleaseEvent(self, event):
        self.mouse_event_previous_pos = self.mouse_event_new_pos
        self.mouse_event_new_pos = QCursor.pos()
        self.update_crop_dimensions()

    def mouseMoveEvent(self, event):
        if self.mouse_event_previous_pos:
            diff = QCursor.pos() - self.mouse_event_previous_pos
            self.move(self.pos() + diff)
            self.mouse_event_previous_pos = QCursor.pos()

    def update_crop_dimensions(self):
        diff_x = (self.parent().width() - self.canvas_controller.scene_image.width()) // 2
        diff_y = (self.parent().height() - self.canvas_controller.scene_image.height()) // 2
        self.left = self.pos().x() - diff_x
        self.right = self.pos().x() + self.width() - diff_x
        self.top = self.pos().y() - diff_y
        self.bottom = self.pos().y() + self.height() - diff_y

    def get_crop_dimensions(self):
        """
        Returns the crop dimensions of the widget that will be used to crop an image
        :return: Top, Bottom, Right, Left column indices
        """
        return self.top, self.bottom, self.right, self.left

    def show(self):
        self.__rubber_band.show()
        super().show()

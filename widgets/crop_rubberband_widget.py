from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QCursor
from PyQt6.QtWidgets import QHBoxLayout, QSizeGrip, QRubberBand, QWidget


class CropRubberBandWidget(QWidget):

    def __init__(self, parent=None):
        super(CropRubberBandWidget, self).__init__(parent=parent)
        self.setWindowFlag(Qt.WindowType.SubWindow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self.__rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.__rubber_band.setPalette(QPalette(Qt.GlobalColor.red))
        self.__rubber_band.setStyleSheet(
            """
                         border: 2px solid red;
                         background-color: rgba(255, 0, 0, 50%);
                 """
        )

        self.mouse_event_previous_pos = None
        self.mouse_event_new_pos = None

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
        self.left = self.pos().x()
        self.right = self.pos().x() + self.width()
        self.top = self.pos().y()
        self.bottom = self.pos().y() + self.height()
        print(self.top, self.left, self.right, self.bottom)

    def get_crop_dimensions(self):
        """
        Returns the crop dimensions of the widget that will be used to crop an image
        :return: Top, Bottom, Right, Left column indices
        """
        return self.top, self.bottom, self.right, self.left

    def show(self):
        self.__rubber_band.show()
        super().show()

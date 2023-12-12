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
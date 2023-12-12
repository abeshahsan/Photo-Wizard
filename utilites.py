from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage


class ValueProperty(QObject):
    valueChanged = pyqtSignal(object)

    def __init__(self, initial_value):
        super().__init__()
        self._value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(new_value)


def cv_image_to_q_pixmap(cv_image):
    height, width, channel = cv_image.shape
    bytes_per_line = channel * width
    q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(q_image)
    return pixmap

import numpy as np
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


def pixmap_to_numpy(pixmap):
    image = pixmap.toImage()
    width, height = image.width(), image.height()
    buffer = image.bits().asarray(height * width * 3)
    return np.array(buffer).reshape((height, width, 3))


def numpy_to_pixmap(numpy_array):
    height, width, channel = numpy_array.shape
    bytes_per_line = 3 * width  # Assuming 3 channels (RGB)
    image = QImage(numpy_array.tobytes(), width, height, bytes_per_line, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)

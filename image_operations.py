import numpy as np
from PyQt6.QtGui import QImage, QPixmap


def q_image_to_numpy(q_image):
    width, height = q_image.width(), q_image.height()
    buffer = q_image.bits().asarray(height * width * 3)
    return np.array(buffer).reshape((height, width, 3))


def numpy_to_q_image(numpy_array):
    height, width, channel = numpy_array.shape
    bytes_per_line = 3 * width  # Assuming 3 channels (RGB)
    return QImage(numpy_array.tobytes(), width, height, bytes_per_line, QImage.Format.Format_RGB888)

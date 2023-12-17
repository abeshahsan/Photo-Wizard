import sys

import numpy as np
from PyQt6.QtGui import QImage, QPixmap

import copy

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene


def q_image_to_numpy(q_image):
    width, height = q_image.width(), q_image.height()
    # Convert QImage to a format compatible with NumPy
    buffer = q_image.constBits().asarray(height * width * 4)  # Assuming 4 bytes per pixel (RGBA)
    arr = np.frombuffer(buffer, np.uint8).reshape((height, width, 4))  # Reshape buffer to image dimensions
    return arr[:, :, :3].copy()  # Return RGB channels and make a copy


def numpy_to_q_image(numpy_array):
    height, width, channel = numpy_array.shape
    bytes_per_line = width * channel  # Calculate bytes per line
    # Create QImage from NumPy array data with RGB channels
    q_img = QImage(numpy_array.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
    return q_img.copy()  # Return a copy to prevent memory issues


def crop_image(q_image, left, top, right, bottom):
    # crop the image and return a NEW image.
    # don't change the passed one
    return QImage()  # change the statement


def blur_image(q_image):
    numpy_array = q_image_to_numpy(q_image)

    new_image = numpy_to_q_image(numpy_array)
    return new_image  # change the statement


def sharpen_image(q_image):
    # crop the image and return a NEW image.
    # don't change the passed one
    return QImage()  # change the statement


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Load the image
    image_path = "Kena.png"
    image = QImage(image_path)
    blurred_image = blur_image(image)
    pixmap = QPixmap(blurred_image)

    # Check if the image was loaded successfully
    if not pixmap.isNull():
        # Add the image to the scene
        scene.addPixmap(pixmap)
    else:
        print("Failed to load the image")

    # Create a QGraphicsView to display the scene
    view = QGraphicsView(scene)
    view.show()
    app.exec()

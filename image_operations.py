import sys

import numpy as np
from PyQt6.QtGui import QImage, QPixmap

import copy

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene


def q_image_to_numpy(q_image):
    """
    Converts a PyQT6 QImage to a Numpy array
    :param q_image: QImage object
    :return: Numpy array
    """
    width, height = q_image.width(), q_image.height()
    # Convert QImage to a format compatible with NumPy
    buffer = q_image.constBits().asarray(height * width * 4)  # Assuming 4 bytes per pixel (RGBA)
    arr = np.frombuffer(buffer, np.uint8).reshape((height, width, 4))  # Reshape buffer to image dimensions
    return arr[:, :, :3].copy()  # Return RGB channels and make a copy


def numpy_to_q_image(numpy_array):
    """
    Converts a Numpy array to a PyQT6 QImage
    :param numpy_array: Numpy array
    :return: QImage object
    """
    height, width, channel = numpy_array.shape
    bytes_per_line = width * channel  # Calculate bytes per line
    # Create QImage from NumPy array data with RGB channels
    q_img = QImage(numpy_array.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
    return q_img.copy()  # Return a copy to prevent memory issues


def crop_image(q_image, top, bottom, right, left):
    """
    Crops an image (PyQT6 QImage object) and returns a copy of the cropped image. Does not affect the original image.
    The function converts it into a numpy array and crops it according to:
        - start and end rows
        - start and end columns
    :param q_image: QImage object
    :param top: the starting row of the numpy array to crop
    :param bottom: the ending row of the numpy array to crop
    :param right: the ending column of the numpy array to crop
    :param left: the starting column of the numpy array to crop
    :return: a copy of the cropped image
    """
    # crop the image and return a NEW image.
    # don't change the provided one
    return QImage()  # change the statement


def blur_image(q_image):
    """
    Blurs an image (PyQT6 QImage object) and returns a copy of the blurred image. Does not affect the original.
    It converts it into a numpy array and performs some blurring operations.
    :param q_image: QImage object
    :return: a copy of the blurred image
    """
    numpy_array = q_image_to_numpy(q_image)

    height, width, _ = numpy_array.shape
    new_image = np.zeros_like(numpy_array, dtype=np.float32)

    radius = 5
    sigma = max(radius / 2.0, 1.0)
    kernel_width = int(2 * radius) + 1

    kernel = np.zeros((kernel_width, kernel_width))
    kernel_sum = 0.0

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            exponent_numerator = -(x * x + y * y)
            exponent_denominator = 2.0 * sigma * sigma

            e_expression = np.exp(exponent_numerator / exponent_denominator)
            kernel_value = e_expression / (2.0 * np.pi * sigma * sigma)

            kernel[x + radius, y + radius] = kernel_value
            kernel_sum += kernel_value

    kernel /= kernel_sum

    for x in range(radius, height - radius):
        for y in range(radius, width - radius):
            for c in range(3):
                value = 0.0
                for kernel_x in range(-radius, radius + 1):
                    for kernel_y in range(-radius, radius + 1):
                        kernel_value = kernel[kernel_x + radius, kernel_y + radius]
                        value += numpy_array[x - kernel_x, y - kernel_y, c] * kernel_value

                new_image[x, y, c] = value

    new_image = new_image.astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image  # change the statement


def sharpen_image(q_image):
    """
    Sharpens an image (PyQT6 QImage object) and returns a copy of the sharpened image. Does not affect the original.
    It converts it into a numpy array and performs some sharpening operations.
    :param q_image: QImage object
    :return: a copy of the sharpened image
    """
    # crop the image and return a NEW image.
    # don't change the passed one
    return QImage()  # change the statement


"""
To test the functions above.
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Load the image
    image_path = "hoi.jpg"
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

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


def crop(q_image, top, bottom, right, left):
    """
    Crops an image (PyQT6 QImage object) and returns a copy of the cropped image. Does not affect the original image. \n
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


def blur(q_image):
    """
    Blurs an image (PyQT6 QImage object) and returns a copy of the blurred image. Does not affect the original.\n
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
            # Extract the region of interest from the input image
            region = numpy_array[x - radius:x + radius + 1, y - radius:y + radius + 1, :]

            # Perform element-wise multiplication with the kernel and sum the result along both axes
            new_image[x, y, :] = np.sum(region * kernel[:, :, np.newaxis], axis=(0, 1))

    new_image = new_image.astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image  # change the statement


def sharpen(q_image):
    """
    Sharpens an image (PyQT6 QImage object) and returns a copy of the sharpened image. Does not affect the original.\n
    It converts it into a numpy array and performs some sharpening operations.
    :param q_image: QImage object
    :return: a copy of the sharpened image
    """
    # crop the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


def change_brightness(q_image):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some brightness operations.
    :param q_image: QImage object
    :return: a copy of the image with changed brightness
    """
    # increase the brightness of the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


def change_contrast(q_image):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some contrast operations.
    :param q_image: QImage object
    :return: a copy of the image with changed contrast
    """
    # increase the contrast of the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


def change_saturation(q_image):
    """
    Changes the saturation of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some saturation operations.
    :param q_image: QImage object
    :return: a copy of the image with changed saturation
    """
    # increase the saturation of the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


def change_exposure(q_image):
    """
    Changes the exposure of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some exposure operations.
    :param q_image: QImage object
    :return: a copy of the image with changed exposure
    """
    # increase the exposure of the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


def change_warmth(q_image):
    """
    Changes the warmth of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some warmth operations.
    :param q_image: QImage object
    :return: a copy of the image with changed warmth
    """
    # increase the warmth of the image and return a NEW image.
    # don't change the passed one
    return q_image  # change the statement


"""
To test the functions above.
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Load the image
    image_path = "C:/Users/Dell/Pictures/bg.jpg"
    image = QImage(image_path)
    blurred_image = blur(image)
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

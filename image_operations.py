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
    Sharpens an image (PyQt6 QImage object) and returns a copy of the sharpened image. Does not affect the original.
    It converts it into a numpy array and performs some sharpening operations.
    :param q_image: QImage object
    :return: a copy of the sharpened image
    """
    numpy_array = q_image_to_numpy(q_image)

    height, width, _ = numpy_array.shape
    new_image = np.zeros_like(numpy_array, dtype=np.float32)

    # Create a Laplacian kernel for sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    for x in range(1, height - 1):
        for y in range(1, width - 1):
            # Extract the region of interest from the input image
            region = numpy_array[x - 1:x + 2, y - 1:y + 2, :]

            # Perform element-wise multiplication with the kernel and sum the result along both axes
            new_image[x, y, :] = np.sum(region * kernel[:, :, np.newaxis], axis=(0, 1))

    # Clip values to be within the valid range [0, 255]
    new_image = np.clip(new_image, 0, 255)

    new_image = new_image.astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def change_brightness(q_image):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some brightness operations.
    :param q_image: QImage object
    :return: a copy of the image with changed brightness
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.int16)
    brightness_factor = 20

    # Add brightness factor and clip to [0, 255] range
    new_image = np.clip(numpy_array + brightness_factor, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def change_contrast(q_image):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some contrast operations.
    :param q_image: QImage object
    :return: a copy of the image with changed contrast
    """
    numpy_array = q_image_to_numpy(q_image)
    contrast_factor = 1.4  # better if within 1-3

    # Apply contrast operation without explicit loops
    new_image = (np.power(numpy_array / 255.0, contrast_factor) * 255.0).astype(np.uint8)

    new_image = numpy_to_q_image(new_image)
    return new_image


def rgb_to_hsv(rgb):
    """
    Convert RGB values to HSV.
    """
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    max_val = np.max(rgb, axis=-1)
    min_val = np.min(rgb, axis=-1)

    delta = max_val - min_val

    # Hue calculation
    hue = np.zeros_like(max_val)

    non_zero_delta = delta != 0
    is_red = (max_val == r) & non_zero_delta
    is_green = (max_val == g) & non_zero_delta
    is_blue = (max_val == b) & non_zero_delta
    
    hue[is_red] = (60 * ((g[is_red] - b[is_red]) / delta[is_red] + 6)) % 360
    hue[is_green] = (60 * ((b[is_green] - r[is_green]) / delta[is_green] + 2)) % 360
    hue[is_blue] = (60 * ((r[is_blue] - g[is_blue]) / delta[is_blue] + 4)) % 360

    # Saturation calculation
    saturation = np.zeros_like(max_val)
    saturation[non_zero_delta] = delta[non_zero_delta] / max_val[non_zero_delta]

    # Value calculation
    value = max_val

    return np.stack([hue, saturation, value], axis=-1)

def hsv_to_rgb(hsv):
    """
    Convert HSV values to RGB.
    """
    hue, saturation, value = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    c = value * saturation
    x = c * (1 - np.abs((hue / 60) % 2 - 1))
    m = value - c

    rgb_prime = np.zeros_like(hsv)

    mask_0 = (0 <= hue) & (hue < 60)
    mask_1 = (60 <= hue) & (hue < 120)
    mask_2 = (120 <= hue) & (hue < 180)
    mask_3 = (180 <= hue) & (hue < 240)
    mask_4 = (240 <= hue) & (hue < 300)
    mask_5 = (300 <= hue) & (hue < 360)

    rgb_prime[..., 0] = np.where(mask_0, c, np.where(mask_1, x, np.where(mask_2, 0, np.where(mask_3, x, np.where(mask_4, c, np.where(mask_5, x, 0)))))) + m
    rgb_prime[..., 1] = np.where(mask_0, x, np.where(mask_1, c, np.where(mask_2, c, np.where(mask_3, x, np.where(mask_4, 0, np.where(mask_5, c, x)))))) + m
    rgb_prime[..., 2] = np.where(mask_0, 0, np.where(mask_1, 0, np.where(mask_2, x, np.where(mask_3, c, np.where(mask_4, c, np.where(mask_5, x, 0)))))) + m

    return (rgb_prime * 255).astype(np.uint8)

def change_saturation(q_image):
    """
    Changes the saturation of an image (PyQt6 QImage object) and returns a copy of the image.
    Does not affect the original.
    It converts it into a numpy array and performs some saturation operations.
    :param q_image: QImage object
    :return: a copy of the image with changed saturation
    """
    # Convert QImage to NumPy array
    numpy_array = q_image_to_numpy(q_image).astype(np.float64)

    saturation_factor = 1

    # Convert RGB to HSV color space
    hsv_image = rgb_to_hsv(numpy_array)

    # Modify saturation channel
    hsv_image[..., 1] = np.clip(hsv_image[..., 1] * saturation_factor, 0, 1)

    # Convert back to RGB color space
    new_image = hsv_to_rgb(hsv_image)

    # Clip values to the valid range [0, 255] and convert to uint8
    new_image = np.clip(new_image, 0, 255).astype(np.uint8)

    # Convert NumPy array back to QImage
    new_image_qimage = numpy_to_q_image(new_image)

    return new_image_qimage


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
    image_path = "F:/PythonProject/Updated2/Kena.png"
    image = QImage(image_path)
    blurred_image = change_saturation(image)
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

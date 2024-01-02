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


def change_brightness(q_image, brightness_factor):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some brightness operations.
    :param q_image: QImage object
    :return: a copy of the image with changed brightness
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.int16)

    # Add brightness factor and clip to [0, 255] range
    new_image = np.clip(numpy_array + brightness_factor, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def change_contrast(q_image, contrast_factor):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some contrast operations.
    :param q_image: QImage object
    :return: a copy of the image with changed contrast
    contrast_factor within 1.0 to 2.2
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.int16)

    # Apply contrast adjustment to each RGB channel independently
    new_image = np.clip(((numpy_array - 128) * contrast_factor) + 128, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def rgb_to_hsv(rgb_image):
    """
    Convert RGB image to HSV color space.
    :param rgb_image: RGB image as a NumPy array
    :return: HSV image as a NumPy array
    """
    input_shape = rgb_image.shape
    rgb_image = rgb_image.reshape(-1, 3)
    r, g, b = rgb_image[:, 0], rgb_image[:, 1], rgb_image[:, 2]

    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc

    deltac = maxc - minc
    np.seterr(invalid='ignore')
    s = np.where(maxc != 0, deltac / maxc, 0)  # Avoid division by zero

    deltac[deltac == 0] = 1  # to not divide by zero (those results in any way would be overridden in next lines)
    rc = (maxc - r) / deltac
    gc = (maxc - g) / deltac
    bc = (maxc - b) / deltac

    h = 4.0 + gc - rc
    h[g == maxc] = 2.0 + rc[g == maxc] - bc[g == maxc]
    h[r == maxc] = bc[r == maxc] - gc[r == maxc]
    h[minc == maxc] = 0.0

    h = (h / 6.0) % 1.0
    res = np.dstack([h, s, v])
    return res.reshape(input_shape)


def hsv_to_rgb(hsv_image):
    """
    Convert HSV image to RGB color space.
    :param hsv_image: HSV image as a NumPy array
    :return: RGB image as a NumPy array
    """
    input_shape = hsv_image.shape
    hsv_image = hsv_image.reshape(-1, 3)
    h, s, v = hsv_image[:, 0], hsv_image[:, 1], hsv_image[:, 2]

    i = np.int32(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    rgb = np.zeros_like(hsv_image)
    v, t, p, q = v.reshape(-1, 1), t.reshape(-1, 1), p.reshape(-1, 1), q.reshape(-1, 1)
    rgb[i == 0] = np.hstack([v, t, p])[i == 0]
    rgb[i == 1] = np.hstack([q, v, p])[i == 1]
    rgb[i == 2] = np.hstack([p, v, t])[i == 2]
    rgb[i == 3] = np.hstack([p, q, v])[i == 3]
    rgb[i == 4] = np.hstack([t, p, v])[i == 4]
    rgb[i == 5] = np.hstack([v, p, q])[i == 5]
    rgb[s == 0.0] = np.hstack([v, v, v])[s == 0.0]

    return rgb.reshape(input_shape)


def change_saturation(q_image, saturation_factor):
    """
    Changes the saturation of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.
    It converts it into a numpy array and performs saturation adjustment.
    :param q_image: QImage object
    :param saturation_factor: Saturation factor (e.g., 1.5 for 1.5x saturation)
    :return: a copy of the image with changed saturation
    saturation_factor within 1.0- 1.4
    """
    numpy_array = q_image_to_numpy(q_image)
    hsv_image = rgb_to_hsv(numpy_array)
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 1)
    new_image = hsv_to_rgb(hsv_image).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def change_exposure(q_image, exposure_factor):
    """
    Changes the exposure of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some exposure operations.
    :param q_image: QImage object
    :return: a copy of the image with changed exposure
    exposure_factor within 1.0 to 1.8
    """
    # increase the exposure of the image and return a NEW image.
    # don't change the passed one
    numpy_array = q_image_to_numpy(q_image).astype(np.int16)

    # Apply exposure adjustment to each RGB channel independently
    new_image = np.clip(numpy_array * exposure_factor, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image


def change_warmth(q_image, warmth_factor):
    """
    Changes the warmth of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.\n
    It converts it into a numpy array and performs some warmth operations.
    :param q_image: QImage object
    :return: a copy of the image with changed warmth
    warmth_factor within 1.0-1.2
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.int16)
    new_image = np.zeros_like(numpy_array, dtype=np.int16)

    new_image[:, :, 0] = numpy_array[:, :, 0] / warmth_factor
    new_image[:, :, 1] = numpy_array[:, :, 1]
    new_image[:, :, 2] = numpy_array[:, :, 2] * warmth_factor
    # Clip values to be within the valid range [0, 255]
    new_image = np.clip(new_image, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image

"""
To test the functions above.
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Load the image
    image_path = "F:/UNI_STUFF/5th Sem/Photo-Wizard/Kena.png"
    image = QImage(image_path)
    blurred_image = change_saturation(image, 2.0)
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
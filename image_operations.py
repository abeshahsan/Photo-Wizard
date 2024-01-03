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

    return arr.copy()  # Return a copy to include the alpha channel


def numpy_to_q_image(numpy_array):
    """
    Converts a Numpy array to a PyQT6 QImage
    :param numpy_array: Numpy array
    :return: QImage object
    """
    height, width, channel = numpy_array.shape
    bytes_per_line = width * channel  # Calculate bytes per line
    # Create QImage from NumPy array data with RGBA channels
    q_img = QImage(numpy_array.data, width, height, bytes_per_line, QImage.Format.Format_ARGB32)
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
    print(q_image.size())
    numpy_array = q_image_to_numpy(q_image).astype(np.uint8)
    new_image = numpy_array[top:bottom, left:right]

    new_image = new_image.astype(np.uint8)
    new_image = numpy_to_q_image(new_image)

    # crop the image and return a NEW image.
    # don't change the provided one
    return new_image.copy()  # change the statement


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
    return new_image.copy()  # change the statement


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
    return new_image.copy()


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
    return new_image.copy()


def change_contrast(q_image, contrast_factor):
    """
    Changes the brightness of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.
    It converts it into a numpy array and performs some contrast operations.
    :param q_image: QImage object
    :return: a copy of the image with changed contrast
    contrast_factor within 1.0 to 2.2
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.float32)  # Convert to float32

    # Apply contrast adjustment to each RGB channel independently
    new_image = np.clip(((numpy_array - 128) * contrast_factor) + 128, 0, 255).astype(np.uint8)

    # Convert NumPy array back to QImage
    new_image_qimage = numpy_to_q_image(new_image)

    return new_image_qimage.copy()


def rgba_to_hsv(rgba_image):
    """
    Convert RGBA image to HSV color space.
    :param rgba_image: RGBA image as a NumPy array
    :return: HSV image as a NumPy array
    """
    input_shape = rgba_image.shape
    rgba_image = rgba_image.reshape(-1, 4)
    red, green, blue, alpha = rgba_image[:, 0], rgba_image[:, 1], rgba_image[:, 2], rgba_image[:, 3]

    maxc = np.maximum(np.maximum(red, green), blue)
    minc = np.minimum(np.minimum(red, green), blue)
    v = maxc

    deltac = maxc - minc
    np.seterr(invalid='ignore')
    s = np.where(maxc != 0, deltac / maxc, 0)  # Avoid division by zero

    deltac[deltac == 0] = 1  # to not divide by zero (those results in any way would be overridden in next lines)
    rc = (maxc - red) / deltac
    gc = (maxc - green) / deltac
    bc = (maxc - blue) / deltac

    h = 4.0 + gc - rc
    h[green == maxc] = 2.0 + rc[green == maxc] - bc[green == maxc]
    h[red == maxc] = bc[red == maxc] - gc[red == maxc]
    h[minc == maxc] = 0.0

    h = (h / 6.0) % 1.0
    res = np.dstack([h, s, v, alpha])
    return res.reshape(input_shape)


def hsv_to_rgba(hsv_image):
    """
    Convert HSV image to RGBA color space.
    :param hsv_image: HSV image as a NumPy array
    :return: RGBA image as a NumPy array
    """
    input_shape = hsv_image.shape
    hsv_image = hsv_image.reshape(-1, 4)
    h, s, v, alpha = hsv_image[:, 0], hsv_image[:, 1], hsv_image[:, 2], hsv_image[:, 3]

    i = np.int32(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    rgba = np.zeros_like(hsv_image)
    v, t, p, q, alpha = v.reshape(-1, 1), t.reshape(-1, 1), p.reshape(-1, 1), q.reshape(-1, 1), alpha.reshape(-1, 1)

    rgba[i == 0] = np.hstack([v, t, p, alpha])[i == 0]
    rgba[i == 1] = np.hstack([q, v, p, alpha])[i == 1]
    rgba[i == 2] = np.hstack([p, v, t, alpha])[i == 2]
    rgba[i == 3] = np.hstack([p, q, v, alpha])[i == 3]
    rgba[i == 4] = np.hstack([t, p, v, alpha])[i == 4]
    rgba[i == 5] = np.hstack([v, p, q, alpha])[i == 5]
    rgba[s == 0.0] = np.hstack([v, v, v, alpha])[s == 0.0]

    return rgba.reshape(input_shape)


def change_saturation(argb_image, saturation_factor):
    """
    Changes the saturation of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.
    It converts it into a numpy array and performs saturation adjustment.
    :param argb_image: ARGB image as a NumPy array
    :param saturation_factor: Saturation factor (e.g., 1.5 for 1.5x saturation)
    :return: a copy of the image with changed saturation
    saturation_factor within 1.0-1.4
    """
    argb_image = q_image_to_numpy(argb_image)
    input_shape = argb_image.shape
    alpha, red, green, blue = argb_image[:, :, 0], argb_image[:, :, 1], argb_image[:, :, 2], argb_image[:, :, 3]

    # Convert ARGB to RGBA for HSV conversion
    rgba_image = np.dstack([red, green, blue, alpha])

    # Convert RGBA to HSV
    hsv_image = rgba_to_hsv(rgba_image)

    # Apply saturation adjustment
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 1)

    # Convert HSV back to RGBA
    new_rgba_image = hsv_to_rgba(hsv_image)

    # Stack ARGB channels
    new_argb_image = np.dstack(
        [new_rgba_image[:, :, 3], new_rgba_image[:, :, 0], new_rgba_image[:, :, 1], new_rgba_image[:, :, 2]])

    # Reshape to the original input shape
    new_argb_image = new_argb_image.reshape(input_shape)

    new_argb_image = new_argb_image.astype(np.uint8)

    # Convert the resulting numpy array back to QImage
    new_qimage = numpy_to_q_image(new_argb_image)

    return new_qimage.copy()


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
    numpy_array = q_image_to_numpy(q_image).astype(np.uint16)
    # Apply exposure adjustment to each RGB channel independently
    new_image = np.clip(numpy_array * exposure_factor, 0, 255).astype(np.uint8)
    new_image = numpy_to_q_image(new_image)
    return new_image.copy()


def change_warmth(q_image, warmth_factor):
    """
    Changes the warmth of an image (PyQT6 QImage object) and returns a copy of the image.
    Does not affect the original.
    It converts it into a numpy array and performs some warmth operations.
    :param q_image: QImage object
    :param warmth_factor: Warmth factor (e.g., 1.0 for no change)
    :return: a copy of the image with changed warmth
    warmth_factor within 1.0-1.2
    """
    numpy_array = q_image_to_numpy(q_image).astype(np.float32)

    # Apply warmth adjustment to each RGB channel independently
    new_image = np.zeros_like(numpy_array)
    new_image[:, :, 0] = numpy_array[:, :, 0] / warmth_factor
    new_image[:, :, 1] = numpy_array[:, :, 1]
    new_image[:, :, 2] = numpy_array[:, :, 2] * warmth_factor
    new_image[:, :, 3] = numpy_array[:, :, 3]  # Preserve the alpha channel

    # Clip values to be within the valid range [0, 255]
    new_image = np.clip(new_image, 0, 255).astype(np.uint8)

    # Convert NumPy array back to QImage
    new_image_qimage = numpy_to_q_image(new_image)

    return new_image_qimage.copy()


"""
To test the functions above.
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # Load the image
    image_path = "F:/UNI_STUFF/5th Sem/Photo-Wizard/Kena.png"
    image = QImage(image_path)
    blurred_image = change_saturation(image, 0.8)
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

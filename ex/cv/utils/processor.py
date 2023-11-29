import cv2
import numpy as np


class ImageProcessor(object):
    def __init__(self, window_name, image_name):
        self._window_name = window_name
        self._image_name = image_name
        self._image = cv2.imread(self._image_name)

    def show(self, title=None, image=None):
        if image is None:
            image = self._image
        if title is None:
            title = self._window_name
        cv2.imshow(title, image)

    def resize(self, percent, image=None):
        if image is None:
            image = self._image
        width = int(image.shape[1] * percent / 100)
        height = int(image.shape[0] * percent / 100)
        return cv2.resize(image, (width, height))

    def crop(self, pt_first, pt_second, image=None):
        if image is None:
            image = self._image

        x_top_left, y_top_left = pt_first
        x_bootom_right, y_bottom_right = pt_second

        if x_bootom_right < x_top_left:
            x_bootom_right, x_top_left = x_top_left, x_bootom_right

        if y_bottom_right < y_top_left:
            y_bottom_right, y_top_left = y_top_left, y_bottom_right

        return image[y_top_left:y_bottom_right, x_top_left:x_bootom_right]

    def rotate(self, angle, image=None, scale=1.0):
        if image is None:
            image = self._image

        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        rotate_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        return cv2.warpAffine(image, rotate_matrix, (width, height))

    def contrast_brightness(self, contrast, brightness, image=None):
        if image is None:
            image = self._image
        zeros = np.zeros(image.shape, image.dtype)
        return cv2.addWeighted(image, contrast, zeros, 0, brightness)

    def hue_saturation_value(self, hue, saturation, value, image=None):
        if image is None:
            image = self._image
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        zeros = np.zeros(h.shape, h.dtype)
        h = cv2.addWeighted(h, 1.0, zeros, 0, hue)
        s = cv2.addWeighted(s, 1.0, zeros, 0, saturation)
        v = cv2.addWeighted(v, 1.0, zeros, 0, value)
        hsv_image = cv2.merge((h, s, v))
        return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    def blend(self, blend, alpha, image=None):
        if image is None:
            image = self._image
        blend = cv2.resize(blend, (image.shape[1], image.shape[0]))
        return cv2.addWeighted(image, alpha, blend, 1.0 - alpha, 0)

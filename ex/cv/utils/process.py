import cv2


def convert_bgr2gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def load_gray_image(filename):
    return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)


def split_image(image):
    return cv2.split(image)  # Blue, Green, Red


def convert_gray2bgr(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


def convert_bgr2hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def convert_hsv2bgr(image):
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

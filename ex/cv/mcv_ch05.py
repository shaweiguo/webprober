import os
import cv2
import numpy as np


def simple_threshold(img):
    threshold = 127
    max = 255
    ret, thresh = cv2.threshold(img, threshold, max, cv2.THRESH_BINARY)

    cv2.imshow('Original Image', img)
    cv2.imshow('Threshold Image', thresh)


def adaptive_threshold(img):
    max = 255
    adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    threshold_type = cv2.THRESH_BINARY_INV
    block_size = 11
    c = 2
    thresh = cv2.adaptiveThreshold(img, max, adaptive_method, threshold_type, block_size, c)
    cv2.imshow('Original Image', img)
    cv2.imshow('Adaptive Threshold Image', thresh)


def otsu_threshold(img):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow('Original Image', img)
    cv2.imshow('OTSU Threshold Image', thresh)


def template_matching():
    img_path = "/home/sha/books/Hands-on-ML-Projects-with-OpenCV/data"
    dog_img_path = os.path.join(img_path, "dog.jpg")
    dog_head_img_path = os.path.join(img_path, "dog-head.jpg")

    main_image = cv2.imread(dog_img_path)
    template_image = cv2.imread(dog_head_img_path)

    template_height, template_width, _ = template_image.shape
    result = cv2.matchTemplate(main_image,
                               template_image,
                               cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + template_width,
                        top_left[1] + template_height)
        cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 255), 1)

    cv2.imshow("Result", main_image)


def template_matching1():
    img_path = "/home/sha/books/Hands-on-ML-Projects-with-OpenCV/data"
    dog_img_path = os.path.join(img_path, "dog.jpg")
    dog_head_img_path = os.path.join(img_path, "dog-head.jpg")

    main_image = cv2.imread(dog_img_path, 0)
    main_image_copy = main_image.copy()
    template_image = cv2.imread(dog_head_img_path, 0)

    template_height, template_width, _ = template_image.shape
    result = cv2.matchTemplate(main_image,
                               template_image,
                               cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + template_width,
                        top_left[1] + template_height)
        cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 255), 1)

    cv2.imshow("Result", main_image)


def main():
    # img_path = "/home/sha/Downloads/star.jpg"
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread(img_path, 0)
    # simple_threshold(img)
    # adaptive_threshold(img)
    # otsu_threshold(img)
    template_matching()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

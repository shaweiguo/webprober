import cv2


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


def main():
    img_path = "/home/sha/Downloads/star.jpg"
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(img_path, 0)
    # simple_threshold(img)
    # adaptive_threshold(img)
    otsu_threshold(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

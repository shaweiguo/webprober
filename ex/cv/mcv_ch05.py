import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
import glob

IMAGE_PATH = "/home/sha/books/Hands-on-ML-Projects-with-OpenCV/data"


def simple_threshold(img):
    threshold = 127
    max = 255
    ret, thresh = cv2.threshold(img, threshold, max, cv2.THRESH_BINARY)

    cv2.imshow("Original Image", img)
    cv2.imshow("Threshold Image", thresh)


def adaptive_threshold(img):
    max = 255
    adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    threshold_type = cv2.THRESH_BINARY_INV
    block_size = 11
    c = 2
    thresh = cv2.adaptiveThreshold(
        img, max, adaptive_method, threshold_type, block_size, c
    )
    cv2.imshow("Original Image", img)
    cv2.imshow("Adaptive Threshold Image", thresh)


def otsu_threshold(img):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("Original Image", img)
    cv2.imshow("OTSU Threshold Image", thresh)


def template_matching():
    dog_img_path = os.path.join(IMAGE_PATH, "dog.jpg")
    dog_head_img_path = os.path.join(IMAGE_PATH, "dog-head.jpg")

    main_image = cv2.imread(dog_img_path)
    template_image = cv2.imread(dog_head_img_path)

    template_height, template_width, _ = template_image.shape
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 255), 1)

    cv2.imshow("Result", main_image)


def template_matching1():
    dog_img_path = os.path.join(IMAGE_PATH, "dog.jpg")
    dog_head_img_path = os.path.join(IMAGE_PATH, "dog-head.jpg")

    main_image = cv2.imread(dog_img_path, 0)
    main_image_copy = main_image.copy()
    template_image = cv2.imread(dog_head_img_path, 0)
    w, h = template_image.shape[::-1]
    methods = [
        "cv2.TM_CCOEFF",
        "cv2.TM_CCOEFF_NORMED",
        "cv2.TM_CCORR",
        "cv2.TM_CCORR_NORMED",
        "cv2.TM_SQDIFF",
        "cv2.TM_SQDIFF_NORMED",
    ]

    for m in methods:
        img = main_image_copy.copy()
        method = eval(m)
        res = cv2.matchTemplate(img, template_image, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 5)

        plt.subplot(121)
        plt.imshow(res, cmap="gray")
        plt.title("Matching Result")
        plt.xticks([]), plt.yticks([])
        plt.subplot(122)
        plt.imshow(img, cmap="gray")
        plt.title("Detected Point")
        plt.xticks([]), plt.yticks([])
        plt.suptitle(m)
        plt.show()


def std_hough_line_transform():
    img = cv2.imread(os.path.join(IMAGE_PATH, "chess.png"))
    img = cv2.resize(img, (640, 480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=100)

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("result", img)


def prob_hough_line_transform():
    img = cv2.imread(os.path.join(IMAGE_PATH, "chess.png"))
    img = cv2.resize(img, (640, 480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10
    )

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("result", img)


def hough_circle_transform():
    img = cv2.imread(os.path.join(IMAGE_PATH, "smarties.png"))
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        20,
        param1=100,
        param2=30,
        minRadius=1,
        maxRadius=30,
    )
    detected_circles = np.uint16(np.around(circles))

    for x, y, r in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(output, (x, y), 2, (0, 255, 255), 3)

    cv2.imshow("output", output)


CHECKERBOARD = (6, 9)


def camera_calibration():
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    objpoints = []
    imgpoints = []
    images = glob.glob(os.path.join(IMAGE_PATH, 'checkerboard*.jpg'))
    # gray = None
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
            cv2.imshow('img', img)
            cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    print(f"Camera matrix: {mtx}")
    print(f"Distortion coefficient: {dist}")
    print(f"Rotation Vectors: {rvecs}")
    print(f"Translation Vectors: {tvecs}")


def main():
    # img_path = "/home/sha/Downloads/star.jpg"
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread(img_path, 0)
    # simple_threshold(img)
    # adaptive_threshold(img)
    # otsu_threshold(img)
    # template_matching1()
    # std_hough_line_transform()
    # prob_hough_line_transform()
    # hough_circle_transform()

    camera_calibration()
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

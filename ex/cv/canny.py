import cv2
import numpy as np


def nothing(x):
    pass


def canny_edge_detection():
    lower, upper = 100, 200
    image = cv2.imread("/home/sha/Downloads/animal.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    cv2.namedWindow("Canny")
    cv2.createTrackbar("Lower", "Canny", lower, 500, nothing)
    cv2.createTrackbar("Upper", "Canny", upper, 500, nothing)
    
    cv2.imshow("Original", image)
    cv2.imshow("Gray", gray)
    
    while True:
        lower = cv2.getTrackbarPos("Lower", "Canny")
        upper = cv2.getTrackbarPos("Upper", "Canny")
        canny = cv2.Canny(gray, lower, upper)
        cv2.imshow("Original", canny)
        
        ch = cv2.waitKey(10)
        
        if (ch & 0xFF) == 27:
            break
        elif ch == ord('s'):
            cv2.imwrite("animal_canny.png", canny)
            print("canny image saved.")
    
    cv2.destroyAllWindows()


def dilation(image, ksize=(1, 1)):
    kernel = np.ones(ksize, np.uint8)
    dilation = cv2.dilate(image, kernel, iterations=1)
    cv2.imshow("Original", image)
    cv2.imshow("Dilation", dilation)
    
    while True:
        ch = cv2.waitKey(10)
        if (ch & 0xFF) == 27:
            break
        elif ch == ord('s'):
            cv2.imwrite("/home/sha/tmp/dilation.png", dilation)
            print("dilation image saved.")
    
    cv2.destroyAllWindows()
    return dilation


def erosion(image, ksize=(1, 1)):
    kernel = np.ones(ksize, np.uint8)
    erosion = cv2.erode(image, kernel, iterations=1)
    cv2.imshow("Original", image)
    cv2.imshow("Erosion", erosion)
    
    while True:
        ch = cv2.waitKey(10)
        if (ch & 0xFF) == 27:
            break
        elif ch == ord('s'):
            cv2.imwrite("/home/sha/tmp/erosion.png", erosion)
            print("erosion image saved.")
    
    cv2.destroyAllWindows()
    return erosion


def main():
    image = cv2.imread("/home/sha/Downloads/animal.jpg")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lower, upper = 290, 475
    canny_image = cv2.Canny(gray_image, lower, upper)
    dilation_image = dilation(canny_image, (3, 3))
    erosion(dilation_image, (3, 3))


if __name__ == '__main__':
    # canny_edge_detection()
    main()

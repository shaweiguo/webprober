import cv2


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


if __name__ == '__main__':
    canny_edge_detection()

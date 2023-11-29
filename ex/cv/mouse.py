import cv2
import numpy as np


# for event in dir(cv2):
#     if 'EVENT' in event:
#         print(event)


def mouse_event(event, x, y, img, flags, param):
    print("Event:", event, "Position:", x, y, "Flags:", flags, "Param:", param)
    if event == cv2.EVENT_LBUTTONDOWN:
        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        my_color_image = np.zeros((100, 280, 3),
                                  np.uint8)
        my_color_image[:] = [blue, green, red]
        str_bgr = f"(B,G,R) = ({str(blue)}, {str(green)} , {str(red)})"
        str_xy = f"(X,Y) = ({str(x)}, {str(y)})"
        txt_font = cv2.FONT_HERSHEY_COMPLEX
        txt_color = (255, 255, 255)
        txt_size = 0.6
        cv2.putText(my_color_image, str_xy, (10, 30),
                    txt_font, txt_size, txt_color, 1)
        cv2.putText(my_color_image, str_bgr, (10, 30),
                    txt_font, txt_size, txt_color, 1)
        cv2.imshow('color', my_color_image)


if __name__ == '__main__':
    img = cv2.imread("/home/sha/Downloads/star.jpg")
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_event, param=123)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

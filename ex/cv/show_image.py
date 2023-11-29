import cv2
import numpy as np


# img_path = "/home/sha/Downloads/star.jpg"
# img = cv2.imread(img_path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Color Image", img)
# cv2.imshow("Gray Image", gray)
# video_path = "/home/sha/work/fpr/image/data/butterfly.mp4"
# # video_path = "/home/sha/Downloads/jetbra/config-jetbrains/dasd715"
# cap = cv2.VideoCapture(video_path)
# success, img = cap.read()
# while success:
#     cv2.imshow("Video", img)
#     if cv2.waitKey(15) & 0xFF == 27:
#         break
#     success, img = cap.read()
# cap.release()


def draw_line(image, start, end, color=(255, 255, 255),
              thickness=1, line_type=cv2.LINE_AA):
    cv2.line(image, start, end, color, thickness, line_type)

canvas = np.zeros((380, 480, 3), np.uint8)
canvas[:] = 235, 235, 235
draw_line(canvas,
          start=(100, 100),
          end=(canvas.shape[1] - 100, canvas.shape[0] - 100),
          color=(10, 10, 10),
          thickness=10)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

cv2.destroyAllWindows()

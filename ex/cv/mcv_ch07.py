import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
import glob
import pytesseract
from PIL import ImageGrab


IMAGE_PATH = "/home/sha/books/Hands-on-ML-Projects-with-OpenCV/data"


def camshift_object_tracking():
    cap = cv2.VideoCapture(os.path.join(IMAGE_PATH, "dog.mp4"))
    ret, frame = cap.read()
    x, y, w, h = 300, 200, 100, 100
    track_window = (x, y, w, h)
    roi = frame[y : y + h, x : x + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        cv2.imshow("CAMShift Object Tracking", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def hcc_face_detection():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = cv2.imread(os.path.join(IMAGE_PATH, "smile.jpg"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Face Dection", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def hfcc_eye_detection():
    eye_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")
    img = cv2.imread(os.path.join(IMAGE_PATH, "smile.jpg"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("Eye Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def hfcc_smile_detection():
    cascade = cv2.CascadeClassifier("haarcascade_smile.xml")
    img = cv2.imread(os.path.join(IMAGE_PATH, "smile.jpg"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smiles = cascade.detectMultiScale(gray, scaleFactor=2.1, minNeighbors=12)

    for x, y, w, h in smiles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Smile Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ocr():
    pytesseract.pytesseract.tesseract_cmd = "tesseract"
    cap = cv2.VideoCapture(os.path.join(IMAGE_PATH, "text_vid.webm"))
    cap.set(3, 640)
    cap.set(4, 480)

    def capture_screen(bbox=(300, 300, 1500, 1000)):
        cap_scr = np.array(ImageGrab.grab(bbox))
        cap_scr = cv2.cvtColor(cap_scr, cv2.COLOR_RGB2BGR)
        return cap_scr

    while True:
        timer = cv2.getTickCount()
        ret, img = cap.read()
        if not ret:
            break
        h_img, w_img, _ = img.shape
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split(" ")
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x, h_img - y), (w, h_img - h), (50, 50, 255), 2)
            cv2.putText(
                img,
                b[0],
                (x, h_img - y + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (50, 50, 255),
                2,
            )
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(
            img,
            str(int(fps)),
            (75, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (20, 230, 20),
            2,
        )

        img = cv2.resize(img, (640, 540))
        cv2.imshow("Text Detection", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    # camshift_object_tracking()
    # hcc_face_detection()
    # hfcc_smile_detection()
    ocr()


if __name__ == "__main__":
    main()

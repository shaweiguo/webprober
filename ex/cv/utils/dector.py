import cv2
import numpy as np


class ShapeDector:
    def __init__(self):
        self.epsilon = 0.02
        self.shapes = {
            "Triangle": 3,
            "Square": 4,
            "Pentagon": 5,
            "Hexagon": 6,
            "Circle": 0
        }

    def get_shape(self, vertices, ratio=1.0):
        shape = "Other"
        for (i, (lbl, vrt)) in enumerate(self.shapes.items()):
            if vertices == vrt:
                if vrt == 4:
                    if ratio > 0.95 and ratio < 1.05:
                        shape = "Square"
                    else:
                        shape = lbl
        return shape
    
    def detect(self, contour):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, self.epsilon * perimeter, True)
        _, _, w, h = cv2.boundingRect(approximation)
        vertices = len(approximation)
        shape = self.get_shape(vertices, (float(w) / float(h)))

        return shape, area, perimeter, vertices
    
    def get_bounding_rect(self, contour):
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, self.epsilon * perimeter, True)
        x, y, w, h = cv2.boundingRect(approximation)
        return x, y, w, h
    
    def get_center(self, contour):
        m = cv2.moments(contour)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m10'] / m['m00'])
        return cx, cy
    

class ColorDector:
    def __init__(self) -> None:
        self.color = {
            "Red_1": ([[0, 90, 100], [10, 255, 255]]),
            "Yellow": ([[11, 90, 100], [35, 255, 255]]),
            "Green": ([[36, 90, 100], [70, 255, 255]]),
            "Cyan": ([[71, 90, 100], [100, 255, 255]]),
            "Blue": ([[101, 90, 100], [120, 255, 255]]),
            "Violet": ([[121, 90, 100], [130, 255, 255]]),
            "Magenta":([[131, 90, 100], [159, 255, 255]]),
            "Pink": ([[161, 90, 100], [166, 255, 255]]),
            "Red_2": ([[167, 90, 100], [190, 255, 255]]),
        }
    
    def get_color_label(self, hsv, mask):
        color_label = "Unknown"
        masked_hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
        mean = cv2.mean(masked_hsv, mask=mask)[:3]
        for (i, (label, (lower, upper))) in enumerate(self.color.items()):
            if (np.all(np.greater_equal(mean, lower)) and
                    np.all(np.less_equal(mean, upper))):
                color_label = label

        return color_label, mean

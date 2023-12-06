import cv2
import numpy as np
from skimage import feature as skf
from matplotlib import pyplot as plt


def LBP(image_path):
    image = cv2.imread(image_path, 0)
    original_hist = cv2.calcHist(image, [0], None, [256], [0, 256])
    
    plt.title("Histogram of Original Image")
    plt.plot(original_hist, color='r')
    
    points = 3 * 8
    radius = 3
    lbp = skf.local_binary_pattern(image, points, radius, method='default')
    lnp_hist, _ = np.histogram(lbp, density=True, bins=256, range=(0, 256))
    
    plt.title("Histogram of LBP Image")
    plt.plot(lnp_hist, color='g')
    plt.show()
    
    cv2.imshow("Original Image", image)
    cv2.imshow("LBP Image", lbp)


if __name__ == '__main__':
    image_path = '/home/sha/Downloads/peoples2.jpg'
    
    LBP(image_path)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
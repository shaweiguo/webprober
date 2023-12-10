import numpy as np
import pathlib
import cv2

import tensorflow as tf
import matplotlib.pyplot as plt


train_img_dir = "./chest_xray/train"
test_img_dir = "./chest_xray/test"

data_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255.)

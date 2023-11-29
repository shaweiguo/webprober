import cv2
import utils.processor as processor


def process():
    p = processor.ImageProcessor("Resize, Crop and Rotate", "/home/sha/Downloads/star.jpg")
    p.show()

    resized_image = p.resize(50)
    p.show("Resized -- 50%", resized_image)

    rotated_image = p.rotate(45, resized_image)
    p.show("Rotated -- 45 degree", rotated_image)

    cropped_image = p.crop((300, 10), (600, 310))
    p.show("Cropped", cropped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def change_brightness(x):
    global brightness
    brightness = x - 128


def change_contrast(x):
    global contrast
    contrast = float(x) / 100


def change_hue(value):
    global hue
    hue = value * 2 - 255


def change_saturation(value):
    global saturation
    saturation = value * 2 - 255


def change_value(value):
    global val
    val = value * 2 - 255


def adjust_cb():
    global brightness
    global contrast
    brightness = 0
    contrast = 1.0
    title = "Adjust Brightness and Conrast"

    p = processor.ImageProcessor(title, "/home/sha/Downloads/star.jpg")
    p.show()
    cv2.createTrackbar('Brightness', title, 128, 255, change_brightness)
    cv2.createTrackbar('Contrast', title, 100, 300, change_contrast)

    while True:
        adjusted_image = p.contrast_brightness(contrast, brightness)
        p.show(title, image=adjusted_image)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def adjust_hsv():
    global hue, saturation, val
    hue, saturation, val = 0, 0, 0

    title = "Adjust Hue, Saturation and Value"

    p = processor.ImageProcessor(title, "/home/sha/Downloads/star.jpg")
    p.show()
    cv2.createTrackbar('Hue', title, 127, 255, change_hue)
    cv2.createTrackbar('Saturation', title, 127, 255, change_saturation)
    cv2.createTrackbar('Value', title, 127, 255, change_value)

    while True:
        adjusted_image = p.hue_saturation_value(hue, saturation, val)
        p.show(title, image=adjusted_image)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def change_alpha(value):
    global alpha
    alpha = float(value) / 100


def blend_tow_images(image_1, image_2):
    global alpha
    alpha = 0.5
    title = "Blend Two Images"

    p = processor.ImageProcessor(title, image_1)
    to_blend = cv2.imread(image_2)
    p.show()
    cv2.createTrackbar('Alpha', title, 50, 100, change_alpha)
    p.show(image=to_blend)
    while True:
        blended_image = p.blend(to_blend, alpha)
        p.show(title, image=blended_image)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    image1 = "/home/sha/Downloads/star.jpg"
    image2 = "/home/sha/Downloads/sea.jpg"
    blend_tow_images(image1, image2)
    # adjust_hsv()

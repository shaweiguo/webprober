import cv2
import numpy as np
import math
import utils.draw as draw



drawing = False
final_color = (255, 255, 255)
drawing_color = (125, 125, 125)


def on_mouse(event, x, y, flags, param):
    global drawing, ctr, radius, img, img_bk

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ctr = x, y
        radius = 0
        draw_circle(img, ctr, radius, drawing_color)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = img_bk.copy()
            radius = calc_radius(ctr, (x, y))
            draw_circle(img, ctr, radius, drawing_color)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        radius = calc_radius(ctr, (x, y))
        draw_circle(img, ctr, radius, final_color, 2, True)
        img_bk = img.copy()


def calc_radius(center, current_point):
    cx, cy = current_point
    tx, ty = center
    return int(math.hypot(cx - tx, cy - ty))


def draw_circle(img, center, radius, color, line_scale=1, is_final=False):
    txt_center = f"ctr=({center[0]}, {center[1]})"
    txt_radius = f"radius={radius}"
    if is_final:
        print(f"Completing circle with {txt_center} and {txt_radius}")
        draw.draw_circle(img, center, 1, color, line_scale)
        draw.draw_circle(img, center, radius, color, line_scale)
        draw.draw_text(img, txt_center,
                       (center[0] - 60, center[1] + 20, 0.5, color))
        draw.draw_text(img, txt_radius,
                       (center[0] - 15, center[1] + 35, 0.5, color))


def print_instruction(img):
    txt_instruction = "Press and hold left key to draw a circle. ESC to exit."
    draw.draw_text(img, txt_instruction, (10, 20), 0.5, (255, 255, 255))
    print(txt_instruction)


def main():
    global img, img_bk

    window_name = "Mouse Drawing Circles"
    img = np.zeros((500, 640, 3), np.uint8)
    print_instruction(img)
    img_bk = img.copy()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse)

    while True:
        cv2.imshow(window_name, img)
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

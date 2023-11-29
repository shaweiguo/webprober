import cv2

# Define the mouse callback function
def mouse_callback(event, x, y, flags, param):
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Retrieve BGR color values of the pixel clicked
        b, g, r = param[y, x]
        # Display the position and BGR color values in the console
        print(f"Mouse clicked at position ({x}, {y}) with BGR color values ({b}, {g}, {r})")


# Load an image
image_path = '/home/sha/Downloads/star.jpg'  # Replace with your image's path
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Image not found.")
else:
    # Create a window
    cv2.namedWindow('Image')

    # Set the mouse callback function for the window with image as an additional parameter
    cv2.setMouseCallback('Image', mouse_callback, param=image)

    # Display the image in the window
    cv2.imshow('Image', image)

    # Wait for a key press indefinitely
    cv2.waitKey(0)

    # Destroy all windows
    cv2.destroyAllWindows()
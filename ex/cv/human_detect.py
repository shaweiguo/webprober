import cv2
import dlib
import sys
import face_recognition
import torch
import torchvision
from torchvision import transforms
from facenet_pytorch import MTCNN


def resize_image(image):
    # image0 = cv2.imread("/home/sha/tmp/yi.jpg")
    # image0 = cv2.imread("/home/sha/Downloads/peoples2.jpg")
    width, height, _ = image.shape
    new_width = 1024
    aspect_ratio = width / height
    new_height = int(new_width * aspect_ratio)
    return cv2.resize(image, (new_width, new_height))


def human_detection(hog, image):
    boxes, weights = hog.detectMultiScale(image, winStride=(8, 8))
    person = 1
    for x, y, w, h in boxes:
        print(f'person {person} found at: {x} {y} {w} {h}')
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            f'person-{person}', (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
            1
        )
        person += 1
        
    return image


def detector1(image):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cv2.imshow("Human Detection Image", human_detection(hog, image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector2(image):
        # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Haar cascade file not loaded properly.")
        sys.exit(1)
    else:
        print("Haar cascade file loaded successfully.")
    # Load the image where you want to perform face detection
    # Convert the image to grayscale, as the Haar Cascade works better on grayscale images
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    print(f"Number of faces detected: {len(faces)}")
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the image with the detected faces
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector3(image):
    # 加载 dlib 的 HOG + SVM 基于面部检测器
    face_detector = dlib.get_frontal_face_detector()

    # 读取图像
    # image = cv2.imread('path_to_your_image.jpg')

    # 转换为灰度图像，因为 dlib 的检测器使用灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用检测器找到图像中的面部
    faces = face_detector(gray_image)
    print(f"Number of faces detected: {len(faces)}")

    # 用矩形标记检测到的面部
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector4(image_path):
    face_detector = dlib.get_frontal_face_detector()
    image = cv2.imread(image_path)
    # image = resize_image(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray_image)
    print(f"Number of faces detected: {len(faces)}")
    # 用矩形标记检测到的面部
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        print(f'person {face} found at: {x} {y} {w} {h}')
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_cnn(iamge_path):
    # 加载基于 CNN 的人脸检测模型
    cnn_face_detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

    # 读取图像
    image = dlib.load_rgb_image(image_path)

    # 检测图像中的面部
    faces = cnn_face_detector(image)

    # 用矩形标记检测到的面部
    for face in faces:
        x, y, w, h = (face.rect.left(), face.rect.top(), face.rect.width(), face.rect.height())
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 显示图像
    # 注意，dlib 使用 RGB 颜色格式，而 OpenCV 使用 BGR，所以如果你想用 OpenCV 显示图像，需要转换颜色格式
    cv2.imshow('Detected Faces', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_fr(image_path):
    image = face_recognition.load_image_file(image_path)

    # 使用 face_recognition 检测图像中的所有人脸
    face_locations = face_recognition.face_locations(image, model="cnn")

    # 转换图像为 OpenCV 的 BGR 格式
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 循环遍历每个检测到的人脸
    for face_location in face_locations:
        # 获取人脸的位置
        top, right, bottom, left = face_location

        # 绘制一个矩形框围绕每个人脸
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_haarcascade(image_path):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(f"face found at {x}, {y}, {w}, {h}")
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    image = resize_image(image)
    cv2.imshow('Face Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_resnet(image_path):
    # 加载预训练的模型（这里使用ResNet50作为示例）
    model = torchvision.models.resnet50(pretrained=True)
    model.eval()

    # 定义转换链，用于预处理图像
    preprocess = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # 加载图像
    # image_path = 'path_to_your_image.jpg'
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 转换图像
    input_tensor = preprocess(image_rgb)
    input_batch = input_tensor.unsqueeze(0)

    # 检查是否有可用的GPU
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    # 使用模型进行人脸识别
    with torch.no_grad():
        output = model(input_batch)

    # TODO: 此处需要添加人脸检测逻辑，例如使用输出生成边界框等。
    # 因为ResNet50不是一个专门的人脸检测模型，你需要一个额外的人脸检测器比如MTCNN。

    # 绘制人脸边界框
    # TODO: 根据人脸检测结果绘制边界框，下面的代码是示例
    for (x, y, w, h) in faces_detected:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_mtcnn(image_path):
    # 创建MTCNN实例
    mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

    # 加载图像
    # image_path = 'path_to_your_image.jpg'
    image = cv2.imread(image_path)
    # MTCNN需要RGB图像，而OpenCV加载的是BGR
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用MTCNN检测人脸
    boxes, _ = mtcnn.detect(image_rgb)

    if boxes is None:
        sys.exit(1)
    # 绘制人脸边界框
    for box in boxes:
        # 提取边界框的坐标
        xmin, ymin, xmax, ymax = [int(b) for b in box]
        print(f'found face at {xmin, ymin, xmax, ymax}')
        # 绘制矩形框
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    image = resize_image(image)
    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detector_resnet50(image_path):
    # 创建MTCNN实例
    mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

    # 加载预训练的人脸识别模型（这里以ResNet-50为例）
    # 注意：实际上应该使用专门为人脸识别训练的模型，如FaceNet, SphereFace等
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
    model.eval()

    # 定义图像预处理步骤
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # 加载图像
    # image_path = 'path_to_your_image.jpg'
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用MTCNN检测人脸
    boxes, _ = mtcnn.detect(image_rgb)

    # 遍历每个检测到的人脸
    for box in boxes:
        # 提取边界框坐标
        xmin, ymin, xmax, ymax = [int(b) for b in box]
        # 裁剪人脸区域
        face = image_rgb[ymin:ymax, xmin:xmax]
        # 转换人脸图像，适配模型输入
        face_tensor = preprocess(face).unsqueeze(0)
        
        # 检查是否有可用的GPU
        if torch.cuda.is_available():
            face_tensor = face_tensor.to('cuda')
            model.to('cuda')
        
        # 使用模型进行人脸识别
        with torch.no_grad():
            output = model(face_tensor)
        
        # TODO: 在这里添加代码来处理输出，例如识别人脸的身份
        
        # 在原始图像上绘制边界框
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    
    image = resize_image(image)

    # 显示图像
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_path = "/home/sha/Downloads/peoples2.jpg"
    # image_path = "/home/sha/tmp/yi.jpg"
    # image = cv2.imread(image_path)
    # image = resize_image(image)
    # detector_resnet50(image_path)
    detector_mtcnn(image_path)

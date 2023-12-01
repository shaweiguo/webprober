# 下面是一个使用Python OpenCV库分析视频文件并打印出现的所有人的示例程序：
import cv2


def detect_people(video_file):
    # 加载人脸检测器
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 打开视频文件
    video = cv2.VideoCapture(video_file)

    # 用于存储已经出现的人
    people = set()

    while True:
        # 读取视频帧
        ret, frame = video.read()

        if not ret:
            break

        # 将帧转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 对每个检测到的人脸进行处理
        for (x, y, w, h) in faces:
            # 绘制人脸矩形框
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 提取人脸图像
            face = frame[y:y+h, x:x+w]

            # 将人脸图像转换为灰度图像
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # 为了减少重复检测，将人脸图像的哈希值作为人的唯一标识
            face_hash = hash(face_gray.tostring())

            # 如果这个人之前没有出现过，则将其添加到已出现人的集合中，并打印
            if face_hash not in people:
                people.add(face_hash)
                print('Person detected!')

        # 显示帧
        cv2.imshow('Video', frame)

        # 按下q键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    video.release()
    cv2.destroyAllWindows()


# 运行示例程序
detect_people('/home/sha/Downloads/jetbra/config-jetbrains/mvez3')
# 在上述示例中，我们首先加载了OpenCV提供的人脸检测器（haarcascade_frontalface_default.xml），然后打开视频文件并逐帧进行处理。对于每一帧，我们使用人脸检测器检测其中的人脸，并将其绘制在帧上。然后，我们提取人脸图像并将其转换为灰度图像。为了减少重复检测，我们将人脸图像的哈希值作为人的唯一标识，如果这个人之前没有出现过，则将其添加到已出现人的集合中，并打印出现的人。最后，我们显示处理后的帧，并通过按下q键来退出循环。

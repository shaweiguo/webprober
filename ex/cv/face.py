# # 这里是使用Python和OpenCV来实现视频文件人脸检测和识别的代码:
# import cv2
# import face_recognition

# # 载入视频文件
# cap = cv2.VideoCapture('video.mp4')  

# # 创建空的face_encodings list来存储所有检测到的面部编码
# face_encodings = []

# # 创建空的names list来存储识别的人名
# names = []

# # 遍历视频的每一帧
# while cap.isOpened():
#     ret, frame = cap.read()
    
#     # 检测出当前帧中的所有面部
#     face_locations = face_recognition.face_locations(frame)
    
#     # 对每个面部提取编码
#     face_encodings_in_this_frame = face_recognition.face_encodings(frame, face_locations)
    
#     # 遍历当前帧中提取的面部编码
#     for face_encoding_in_this_frame in face_encodings_in_this_frame:
      
#         # 查看该面部是否与之前储存的面部相匹配
#         matches = face_recognition.compare_faces(face_encodings, face_encoding_in_this_frame)
      
#         # 如果没有匹配上,则该面部为未知面部
#         if not True in matches:
            
#             # 将该编码加入到face_encodings list
#             face_encodings.append(face_encoding_in_this_frame)
            
#             # 打印出该未知面部
#             print("Unknown person found")
            
#         else:
#             index = matches.index(True)
#             name = names[index]
            
#             print(f'{name} appears in this frame')
            
#     # 更新names list        
#     names = names + ["Unknown" for i in range(len(face_encodings) - len(names))] 

# cap.release()

# # 这个程序的主要步骤是:

# # 遍历视频的每一帧
# # 在当前帧中检测出所有人脸
# # 计算出每个人脸的编码
# # 将该编码与之前存储的所有编码进行对比
# # 如果没有匹配上的就是未知人脸,将其信息存储并打印出来
# # 如果匹配上了,则获取该人脸对应的名字,打印出该人在当前帧中出现

# # 这样就可以实现视频文件中出现的所有人脸的检测和识别,同时对于重复出现的人脸只会打印一次。
# 在PyTorch中实现这个需求，你需要一个预训练的人脸识别模型来检测和识别视频中的人。下面的步骤可以帮助你完成这个任务：


# 准备环境：
# 确保你的环境中安装了PyTorch，OpenCV，以及face_recognition库（这是一个常用的基于dlib的人脸识别库）。


# 加载视频文件：
# 使用OpenCV加载视频文件，并逐帧读取。


# 人脸检测与识别：
# 对于视频中的每一帧，使用人脸检测模型来确定人脸的位置，然后使用一个人脸识别模型来得到一个人脸的编码。


# 人脸比对：
# 将得到的人脸编码与已知的人脸编码进行比对，判断是否为同一个人。如果是新的人脸，则将其加入已知人脸列表。


# 输出结果：
# 打印视频中检测到的人脸列表。


# 下面是一个简单的代码示例，展示了如何实现上面的步骤：
import cv2
import face_recognition
import numpy as np

# 初始化已知人脸编码列表和已知人脸名称列表
known_face_encodings = []
known_face_names = []

# 加载视频
video_capture = cv2.VideoCapture('/home/sha/Downloads/jetbra/config-jetbrains/mvez3')

# 初始化一些变量
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 抓取视频的一帧
    ret, frame = video_capture.read()
    if not ret:
        break

    # 为了加快识别速度，可以将视频帧的大小调整为1/4大小
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # 将BGR图片转换成RGB图片
    rgb_small_frame = small_frame[:, :, ::-1]

    # 只处理每一帧中的每一帧
    if process_this_frame:
        # 找到当前帧中所有的人脸和人脸编码
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 查看这张脸是否与已知人脸匹配
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # 使用距离最近的已知人脸
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # 如果是新的人脸，则添加到已知人脸列表中
            if name == "Unknown":
                known_face_encodings.append(face_encoding)
                name = f"Person {len(known_face_encodings)}"
                known_face_names.append(name)

            face_names.append(name)

    process_this_frame = not process_this_frame

    # 显示结果
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 放大回原来的大小
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 画出人脸框
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 画出人名标签
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 显示最终视频帧
    cv2.imshow('Video', frame)

    # 按 'q' 退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放视频捕获
video_capture.release()
cv2.destroyAllWindows()

# 打印出现过的所有人
print("Detected the following people:")
for name in known_face_names:
    print(name)

# 这段代码已经包含了视频读取、人脸检测、人脸识别和结果展示的所有必要步骤。当然，这只是一个基本的示例。在实际应用中，你可能需要使用更复杂的方法来处理不同的情况，例如不同的光照条件、不同的人脸角度等。此外，你可能还需要训练自己的人脸识别模型以适应特定的应用场景。

import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
from PIL import Image


# 如果有可用的GPU，则使用GPU，否则使用CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 初始化MTCNN和InceptionResnetV1
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# 使用DBSCAN算法进行人脸聚类
dbscan = DBSCAN(eps=0.6, min_samples=5, metric='euclidean')

# 存储人脸特征和帧号
embeddings = []
frame_indices = []

# 加载视频文件
video_path = '/home/sha/tmp/pingpang.mp4'
video_capture = cv2.VideoCapture(video_path)

frame_count = 0
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        break

    # 将图像从BGR转换为RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 检测人脸
    boxes, _ = mtcnn.detect(frame_rgb)

    if boxes is not None:
        # 提取人脸特征
        faces = []
        for box in boxes:
            # 调整边界框，确保它们不会超出图像边界
            x1, y1, x2, y2 = [max(0, int(coord)) for coord in box]
            x2 = min(frame_rgb.shape[1], x2)  # frame_rgb.shape[1] 是图像宽度
            y2 = min(frame_rgb.shape[0], y2)  # frame_rgb.shape[0] 是图像高度
            
            # 如果边界框有效（即宽度和高度大于0）
            if x2 - x1 > 0 and y2 - y1 > 0:
                face = frame_rgb[y1:y2, x1:x2]
                face = Image.fromarray(face)
                face_tensor = mtcnn(face)  # Use MTCNN to align and crop the face

                # Only append the face tensor to the list if it is not None
                if face_tensor is not None:
                    faces.append(face_tensor)
                
        if faces:
            faces = torch.cat(faces).to(device)
            face_embeddings = resnet(faces).detach().cpu()  # Get embeddings as a tensor
            embeddings.extend(face_embeddings)  # Use extend to add all embeddings to the list
            frame_indices.extend([frame_count] * faces.size(0))

    frame_count += 1

# 释放视频捕获对象
video_capture.release()

if embeddings:
    # 将所有人脸特征拼接成一个张量
    embeddings = torch.cat(embeddings).cpu().numpy()
    
    # 使用DBSCAN进行聚类
    cluster_labels = dbscan.fit_predict(embeddings)

    # 计算每个簇的人脸出现次数
    face_counts = defaultdict(int)
    for label in cluster_labels:
        face_counts[label] += 1

    # 打印每个人脸出现的次数
    for label, count in face_counts.items():
        if label != -1:
            print(f"Person {label} appeared {count} times.")

    # 显示每个人脸
    unique_labels = np.unique(cluster_labels)
    for label in unique_labels:
        if label == -1:
            continue
        indices = np.where(cluster_labels == label)[0]
        representative_idx = indices[0]  # 使用第一个索引作为代表
        representative_frame_idx = frame_indices[representative_idx]
        representative_embedding = embeddings[representative_idx]
        
        # 重新加载代表帧并显示标记的人脸
        video_capture = cv2.VideoCapture(video_path)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, representative_frame_idx)
        ret, frame = video_capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, _ = mtcnn.detect(frame_rgb)
            if boxes is not None:
                box = boxes[indices[0]]
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                cv2.imshow(f'Person {label}', frame)
                cv2.waitKey(0)
        video_capture.release()
else:
    print("No faces detected in the video.")

cv2.destroyAllWindows()

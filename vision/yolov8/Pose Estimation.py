import cv2
import torch
from ultralytics import YOLO

# 加载预训练的 YOLOv8 pose 模型
model = YOLO('yolo11m-pose.pt')

# 定义部位颜色
colors = {
    'torso': (0, 255, 255),      # 黄色
    'left_arm': (255, 0, 0),     # 蓝色
    'right_arm': (0, 0, 255),    # 红色
    'left_leg': (255, 165, 0),   # 橙色
    'right_leg': (0, 255, 0)     # 绿色
}

# 定义关键点连接关系
connections = {
    'torso': [(5, 6), (5, 11), (6, 12), (11, 12)],
    'left_arm': [(5, 7), (7, 9)],
    'right_arm': [(6, 8), (8, 10)],
    'left_leg': [(11, 13), (13, 15)],
    'right_leg': [(12, 14), (14, 16)]
}

# 视频路径和输出设置
video_path = 'E:/Desktop/football_robot/code/vision/yolov8/20241103_011125.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("无法打开视频文件")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
output_path = 'output_pose_estimation.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 推理当前帧
    results = model(frame)

    # 遍历每个人体姿态的检测结果
    for result in results:
        if result.keypoints is not None and result.keypoints.xy.numel() > 0:
            for person_id, keypoints in enumerate(result.keypoints.xy):
                # 绘制骨架并过滤遮挡点
                for part, links in connections.items():
                    color = colors[part]
                    for start, end in links:
                        if (result.keypoints.conf[person_id][start] > 0.5 and 
                            result.keypoints.conf[person_id][end] > 0.5):
                            x1, y1 = int(keypoints[start][0]), int(keypoints[start][1])
                            x2, y2 = int(keypoints[end][0]), int(keypoints[end][1])
                            if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                                cv2.line(frame, (x1, y1), (x2, y2), color, thickness=4)

                # 绘制关键点，跳过面部点
                for i in range(5, len(keypoints)):
                    if result.keypoints.conf[person_id][i] > 0.5:
                        x, y = int(keypoints[i][0]), int(keypoints[i][1])
                        if x > 0 and y > 0:
                            cv2.circle(frame, (x, y), radius=5, color=(0, 255, 0), thickness=-1)

    # 写入处理过的帧
    out.write(frame)

    # 实时显示（可选）
    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()

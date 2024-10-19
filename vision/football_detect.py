import cv2
import torch
import os

# 加载 YOLOv5 模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Desktop/football_robot/code/vision/best.pt')

# 打开视频文件
video_path = 'E:/Desktop/football_robot/code/vision/input_video/90_18.4_0.4_0.1.mp4'
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 获取视频的文件名
input_video_name = os.path.splitext(os.path.basename(video_path))[0]

# 获取视频的帧率和尺寸
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置输出视频文件名：output + 输入视频名称
output_video_name = f'output_{input_video_name}.mp4'

# 设置输出视频
out = cv2.VideoWriter(output_video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# 用于存储目标的中心点轨迹
trajectory = []

# 创建一个字典用于存储检测到的目标及其出现次数
detections_history = {}

# 定义每个目标的ID寿命（如果目标持续检测少于这个值则认为是噪声）
max_life = 3  # 3帧内连续检测到同一目标则认为有效

# 逐帧读取视频并进行推理
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 推理
    results = model(frame)

    # 筛选置信度大于 0.5 的检测结果
    filtered_results = []
    current_frame_detections = []

    for detection in results.pred[0]:
        if detection[4] > 0.5:  # detection[4] 是置信度
            x1, y1, x2, y2 = detection[0:4]  # 检测框的坐标
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            
            current_frame_detections.append((center_x, center_y))

    # 更新检测历史
    updated_detections_history = {}
    
    # 检查当前帧的每个检测中心是否已在历史中
    for center_x, center_y in current_frame_detections:
        found_existing = False
        
        for (prev_x, prev_y), life in detections_history.items():
            # 如果当前检测的中心点与历史中心点接近（使用简单的欧几里得距离）
            if (abs(center_x - prev_x) < 20) and (abs(center_y - prev_y) < 20):
                updated_detections_history[(center_x, center_y)] = life + 1
                found_existing = True
                break
        
        # 如果没有找到类似的历史点，则记录为新的检测
        if not found_existing:
            updated_detections_history[(center_x, center_y)] = 1
    
    # 过滤掉寿命较短的目标（即短暂出现的噪声）
    for (center_x, center_y), life in updated_detections_history.items():
        if life >= max_life:
            trajectory.append((center_x, center_y))  # 只有寿命足够的目标才加入轨迹

    # 更新历史记录
    detections_history = updated_detections_history

    # 在帧上绘制推理结果
    annotated_frame = results.render()[0].copy()  # 创建一个副本，确保可写

    # 绘制轨迹
    for i in range(1, len(trajectory)):
        if trajectory[i - 1] is None or trajectory[i] is None:
            continue
        # 在每一帧上画出中心点轨迹
        cv2.line(annotated_frame, trajectory[i - 1], trajectory[i], (0, 255, 0), 2)

    # 将绘制的帧写入输出视频
    out.write(annotated_frame)

    # 显示处理的帧（可选）
    cv2.imshow('YOLOv5 Detection with Filtered Trajectory', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()

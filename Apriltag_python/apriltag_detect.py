import cv2
import apriltag as apriltag
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# 初始化 AprilTag 检测器
detector = apriltag.Detector()

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头数据")
        break

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 进行 AprilTag 检测
    results = detector.detect(gray)

    # 遍历检测到的标签并绘制
    for r in results:
        corners = r.corners  # 获取四个角点
        center = r.center  # 获取中心点
        tag_id = r.tag_id  # 获取标签ID

        # 绘制标签的边界
        for i in range(4):
            pt1 = (int(corners[i][0]), int(corners[i][1]))
            pt2 = (int(corners[(i + 1) % 4][0]), int(corners[(i + 1) % 4][1]))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # 绘制中心点
        cv2.circle(frame, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)

        # 在标签上方显示其 ID
        cv2.putText(frame, f"ID: {tag_id}", (int(center[0]) - 10, int(center[1]) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 显示结果
    cv2.imshow('AprilTag Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()

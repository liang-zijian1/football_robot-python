import cv2
import os

# 创建保存图片的文件夹
save_dir = 'calibration_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 打开摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("按 's' 拍照并保存, 按 'q' 退出程序")

image_count = 0

while True:
    # 读取摄像头图像
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头数据")
        break

    # 显示图像
    cv2.imshow('Camera', frame)

    # 等待用户输入
    key = cv2.waitKey(1)
    
    if key == ord('s'):  # 按下 's' 保存图像
        image_path = os.path.join(save_dir, f'calibration_{image_count}.jpg')
        cv2.imwrite(image_path, frame)
        print(f"图片已保存: {image_path}")
        image_count += 1

    elif key == ord('q'):  # 按下 'q' 退出
        break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()

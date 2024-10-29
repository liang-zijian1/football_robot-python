import cv2
import numpy as np
import glob

# 设置棋盘格的尺寸 (例如 9x6)
chessboard_size = (8, 6)
square_size = 26.0  # 每个方块的实际尺寸（以相同单位计量，比如cm）

# 准备标定用的棋盘格的3D点（假设棋盘位于z=0的平面上）
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# 存储标定图像的3D点和2D点
obj_points = []  # 3D点
img_points = []  # 2D图像点

# 读取所有标定图片
images = glob.glob(r'e:\Desktop\football_robot\code\calibration_images\*.jpg')

# 遍历每张图片，寻找棋盘格角点
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 找到棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
    # 如果找到，添加对象点和图像点
    if ret:
        obj_points.append(objp)
        img_points.append(corners)
        
        # 可视化角点
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Chessboard Corners', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# 标定摄像头
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# 保存标定结果
print("Camera Matrix:\n", camera_matrix)
print("Distortion Coefficients:\n", dist_coeffs)

# 3. 校正视频流中的图像
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 使用标定参数校正畸变
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, camera_matrix)
    
    # 显示原图和校正后的图像
    cv2.imshow('Original', frame)
    cv2.imshow('Undistorted', undistorted_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import torch
from networktables import NetworkTables
import time

# Initialize NetworkTables client
NetworkTables.initialize(server='roborio-254-frc.local')  # 替换为RoboRIO IP或队伍号
table = NetworkTables.getTable("vision")

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Desktop/football robot/code/vision/best.pt')

# Open video source (0 for webcam, or provide path to video file)
video_path = 'test.mp4'
cap = cv2.VideoCapture(video_path)

# List to store trajectory points
trajectory = []

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Unable to open video source.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model(frame)

    # Filter results by confidence threshold (e.g., 0.5)
    filtered_results = []
    for *box, conf, cls in results.pred[0].cpu().numpy():
        if conf > 0.5:
            filtered_results.append(box)

    # Send the coordinates of the detected object to NetworkTables
    if filtered_results:
        x1, y1, x2, y2 = filtered_results[0]  # Assuming the first detected object is the target
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        table.putNumber('centerX', center_x)
        table.putNumber('centerY', center_y)

        # Append the center of the detected object to the trajectory
        trajectory.append((center_x, center_y))

    # Annotate frame with detection results
    annotated_frame = results.render()[0]

    # Draw trajectory on the frame
    for i in range(1, len(trajectory)):
        cv2.line(annotated_frame, trajectory[i - 1], trajectory[i], (0, 255, 0), 2)

    # Display the annotated frame
    cv2.imshow('Object Detection and Tracking', annotated_frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a small delay (optional)
    time.sleep(0.05)

# When everything done, release the capture and close any open windows
cap.release()
cv2.destroyAllWindows()

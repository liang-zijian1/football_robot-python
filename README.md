# football_robot-python
# 足球机器人 Python 项目

## 概述
该项目实现了一个使用 Python 控制的足球机器人，具备底盘运动、射球和视觉目标检测功能。项目还包括 MATLAB 仿真，模拟球体的出射轨迹，综合考虑空气阻力和马格努斯力。

## 功能

### 机器人控制
- **底盘运动控制**：使用 TalonFX 电机和 PID 控制器实现精准的机器人底盘移动和转向。
- **射球系统**：通过控制双电机速度调节足球的发射角度和力度。
- **LED 状态指示**：通过 LED 控制反馈机器人当前状态，例如速度稳定时绿灯闪烁。

### 视觉跟踪
- **YOLOv5 目标检测**：通过 YOLOv5 检测足球位置，计算并绘制球体的实际运动轨迹。

### MATLAB 仿真
- **球体轨迹仿真**：使用 MATLAB 仿真球体出射后的空气动力学行为，考虑到空气阻力和马格努斯效应，通过数值解法计算其轨迹。

## 文件结构
- `main_control_code/`：主控制程序，处理机器人底盘和射球的运动控制。
- `vision/`：包含 YOLOv5 实现的视觉检测代码，用于跟踪球体。
- `matlab_simulation/`：基于 MATLAB 的物理仿真代码，用于模拟球体的复杂运动轨迹。

## 安装

1. 克隆项目仓库：
   ```bash
   git clone https://github.com/liang-zijian1/football_robot-python.git
2. 安装环境依赖
    ```bash
    pip install -r requirements.txt
    注意：必须使用python3.12版本
## 使用
- 请参考FRC竞赛机器人官方文档
- https://docs.wpilib.org/en/stable/docs/zero-to-robot/introduction.html

   



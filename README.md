# football_robot-python
足球机器人 Python 项目
概述
该项目使用 Python 编程实现一个足球机器人，具有复杂的运动控制、射球系统和目标检测等功能。同时，项目包括基于 MATLAB 的物理仿真，模拟球体出射后的空气动力学行为（阻力和马格努斯效应），以及基于 YOLOv5 的目标检测，用于追踪球体实际轨迹。

功能
机器人控制
运动控制（底盘）：使用 TalonFX 电机结合 PID 控制，实现高精度的底盘运动和转向。
射球系统：包括双电机驱动的射球系统，可通过调节电机速度和方向来控制球的射出角度和速度。
LED 状态显示：通过编程控制 LED 进行状态反馈，如系统就绪、速度稳定等。
视觉跟踪
YOLOv5 目标检测：通过视觉检测足球的位置，并绘制其在视频中的轨迹。检测每帧中的球并计算其中心点，随后平滑连接各个点，得出球的实际运动轨迹。
MATLAB 物理仿真
球体轨迹仿真：基于球体在空气中的动力学模型，使用数值解方法计算出球在 x, y, z 三个方向上的运动轨迹，考虑空气阻力和马格努斯力。
数值解法：利用 MATLAB 对球体受力分析，使用数值积分解出复杂轨迹。
文件结构
main_control_code/：包含主控制代码，处理底盘、射球等控制任务。
vision/：基于 YOLOv5 的视觉检测代码，进行目标检测和轨迹跟踪。
matlab_simulation/：包含 MATLAB 仿真代码，进行球体轨迹的物理仿真。
安装
克隆项目仓库：

bash
复制代码
git clone https://github.com/liang-zijian1/football_robot-python.git
安装 Python 依赖：

bash
复制代码
pip install -r requirements.txt
如果需要使用 MATLAB 仿真，请确保 MATLAB 已正确配置。

使用
启动机器人主控制程序：

bash
复制代码
python main_control_code/main.py
运行 MATLAB 仿真： 打开 matlab_simulation 文件夹中的脚本，运行球体轨迹仿真。


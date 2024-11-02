from networktables import NetworkTables
from phoenix5 import ControlMode

class AutoAim:
    """管理自瞄功能的类"""

    def __init__(self, yaw, pitch, controller, table):
        self.yaw = yaw
        self.pitch = pitch
        self.controller = controller
        self.table = table
        self.aiming_mode = False  # 初始状态为非自瞄模式
        self.previous_lb_state = False  # 记录上一次LB键的状态

        # 限位设定
        self.yaw_min_position = 1870
        self.yaw_max_position = 2900
        self.pitch_min_position = 25
        self.pitch_max_position = 421
        self.dead_zone = 3  # 死区值，小于这个值的误差不再调整

        # 增量系数，用于控制每次调整的幅度
        self.k_yaw = 0.7  # Yaw 轴增量系数
        self.d_yaw = 0.3  # Yaw 轴的 D 控制系数
       
        self.k_pitch = 0.8  # Pitch 轴增量系数
        self.d_pitch = 0.08  # Pitch 轴的 D 控制系数

        # 上一次的误差值
        self.last_x_offset = 0
        self.last_y_offset = 0

    def toggle_aiming_mode(self):
        """切换自瞄模式"""
        current_lb_state = self.controller.getLeftBumper()
        if current_lb_state and not self.previous_lb_state:
            self.aiming_mode = not self.aiming_mode
        self.previous_lb_state = current_lb_state  # 更新 LB 按键状态

    def auto_aim(self):
        """执行自瞄调整逻辑"""
        if not self.aiming_mode:
            return
        
        # 获取 offset 值
        x_offset = self.table.getNumber("x_offset", None)
        y_offset = self.table.getNumber("y_offset", None)

        # 如果没有检测到标签，不执行任何动作
        if x_offset == 0 or y_offset == 0:
            self.yaw.init_motor()
            self.pitch.motor_init()
            return

        # 死区过滤：如果偏移量小于阈值，停止控制
        if abs(x_offset) < self.dead_zone and abs(y_offset) < self.dead_zone:
            return

        # 计算增量调整量
        yaw_increment = x_offset * self.k_yaw
        pitch_increment = y_offset * self.k_pitch

        # 计算微分项，用于抑制震荡
        yaw_d_term = self.d_yaw * (x_offset - self.last_x_offset)
        pitch_d_term = self.d_pitch * (y_offset - self.last_y_offset)

        # 将增量和微分项结合到控制指令中
        yaw_adjustment = yaw_increment + yaw_d_term
        pitch_adjustment = pitch_increment + pitch_d_term

        # 更新误差值，供下次微分计算
        self.last_x_offset = x_offset
        self.last_y_offset = y_offset

        # 获取当前电机位置
        current_yaw_position = self.yaw.yaw_motor.getSelectedSensorPosition()
        current_pitch_position = self.pitch.pitch_motor1.getSelectedSensorPosition()

        # 增量调整电机位置
        new_yaw_position = current_yaw_position + yaw_adjustment
        new_pitch_position = current_pitch_position - pitch_adjustment

        # 检查限位，防止电机超出设定的范围
        if self.yaw_min_position <= new_yaw_position <= self.yaw_max_position:
            self.yaw.yaw_motor.set(ControlMode.Position, new_yaw_position)

        if self.pitch_min_position <= new_pitch_position <= self.pitch_max_position:
            self.pitch.pitch_motor1.set(ControlMode.Position, new_pitch_position)
            self.pitch.pitch_motor2.set(ControlMode.Follower, self.pitch.pitch_motor1.getDeviceID())

        #print(f"Aiming Mode ON: x_offset={x_offset}, y_offset={y_offset}, yaw_adjustment={yaw_adjustment}, pitch_adjustment={pitch_adjustment}")

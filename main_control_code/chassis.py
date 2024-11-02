from phoenix6.hardware import Pigeon2, TalonFX, CANcoder
from phoenix6.controls import DutyCycleOut, TorqueCurrentFOC, VoltageOut, PositionDutyCycle, PositionVoltage, PositionTorqueCurrentFOC, VelocityDutyCycle, VelocityVoltage, VelocityTorqueCurrentFOC, Follower,MusicTone
from wpilib import XboxController,SmartDashboard
import math

class Speed:
    def __init__(self, vec_v, vec_yaw):
        self.m_vec_v = vec_v
        self.m_vec_yaw = vec_yaw


class SpeedT:
    def __init__(self):
        self.last_speed = Speed(0, 0)
        self.present_speed = Speed(0, 0)


def add_vectors(a, b):
    x = a.m_vec_v * math.cos(a.m_vec_yaw) + b.m_vec_v * math.cos(b.m_vec_yaw)
    y = a.m_vec_v * math.sin(a.m_vec_yaw) + b.m_vec_v * math.sin(b.m_vec_yaw)
    result_v = math.sqrt(x ** 2 + y ** 2)
    result_yaw = math.atan2(y, x)
    return Speed(result_v, result_yaw)


def non_leaner_control(inputs):
    inputs = 0.31083769050760857 * math.sinh(0.5859152429745125 * math.sinh(1.8849555921538759 * inputs))
    return inputs


class Vec3d:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0


class Wheel:
    def __init__(self, drive_id, servo_id, coder_id, offset):
        self.m_offset = offset
        self.servo_gear = 12.84375
        self.offset_inter = 0
        self.drive_motor = TalonFX(drive_id)
        self.servo_motor = TalonFX(servo_id)
        self.servo_coder = CANcoder(coder_id)

    def set_target_angle_zero(self, rotation):
        err_rota = rotation + self.servo_coder.get_absolute_position().value_as_double - self.m_offset
        target = self.servo_motor.get_position().value_as_double - err_rota * self.servo_gear
        self.servo_motor.set_control(PositionDutyCycle(target))
        self.offset_inter = target
        # SmartDashboard.putNumber("target", target)

    def set_target_angle(self, rotation):
        rotation = rotation * self.servo_gear
        self.servo_motor.set_control(PositionDutyCycle(rotation + self.offset_inter))

    def wheel_percent_ctrl(self, percent):
        self.drive_motor.set_control(DutyCycleOut(-percent))


class Helper:
    def __init__(self):
        self.is_dead_band = True

    def death_judge(self, n, m, p_uni):
        temp = Vec3d()
        if (n ** 2 + m ** 2 > 0.1 ** 2) or abs(p_uni) > 0.1:
            if n ** 2 + m ** 2 > 0.1 ** 2:
                temp.x = n
                temp.y = m
            else:
                temp.x = 0
                temp.y = 0
            if abs(p_uni) > 0.1:
                temp.w = p_uni
            else:
                temp.w = 0
            self.is_dead_band = False
            return temp
        else:
            temp.x = 0
            temp.y = 0
            temp.w = 0
            self.is_dead_band = True
            return temp

    def get_dead_band(self):
        return self.is_dead_band


def dead_bond_filter(axis_val):
    if 0.06 > axis_val > -0.06:
        axis_val = 0
    return axis_val


def cap_filter(value, peak):
    if value < -peak:
        return -peak
    if value > +peak:
        return +peak
    return value


def correct_yaw(_target_angle_gyro, _current_angle, _current_angular_rate):
    # grab some input data from Pigeon and gamepad
    rcw_error = (_target_angle_gyro - _current_angle) * (-0.02) - _current_angular_rate * (-0.0012)  # PD没有I control
    rcw_error = cap_filter(rcw_error, 0.75)
    rcw_error = dead_bond_filter(rcw_error)
    return rcw_error

class Chassis:
    def __init__(self):
        # 车辆固有属性
        self.CAR_LENGTH = 0.5
        self.CAR_WIDTH = 0.5
        self.SPEED_V_LIMIT = 1.0
        self.SPEED_W_LIMIT = 1.0

        self.Circle_rad = math.atan(self.CAR_LENGTH / self.CAR_WIDTH)

        # 车辆状态变量
        self.car_V = 0.0
        self.car_yaw = 0.0
        self.PTZ_yaw = 0.0
        self.pre_speed_w = 0.0
        self.target_angle_gyro = 0.0
        self.gyro_last_yaw = 0.0
        self.is_reset = 0

        # 轮组状态变量
        self.wheel_speeds = [Speed(0, 0), Speed(0, 0), Speed(0, 0), Speed(0, 0)]
        self.wheel_lp = [SpeedT(), SpeedT(), SpeedT(), SpeedT()]
        self.wheel_info = [Speed(0, 0), Speed(0, 0), Speed(0, 0), Speed(0, 0)]

        # 轮组硬件属性及硬件声明
        wheel_data = [
            (1, 2, 3, 0.316162),  # FL
            (4, 5, 6, -0.467285),  # FR
            (7, 8, 9, -0.118652),  # BL
            (10, 11, 12, 0.313721)  # BR
        ]
        self.GIM_Wheel = [Wheel(drive_id, servo_id, coder_id, offset) for drive_id, servo_id, coder_id, offset in
                          wheel_data]
        self.gyro = Pigeon2(0)

    def calc_speed(self, speed_x, speed_y, speed_w, is_dead_area):
        current_angle = self.gyro.get_yaw().value_as_double-90  # remain bug,得到deg
        #print(self.gyro.get_yaw().value_as_double)
        # 得到角度变化率，用于PID的D参数
        current_angular_rate = self.gyro.get_angular_velocity_z_world().value_as_double  # remain bug
        #print(current_angular_rate)
        # 将角度转化为弧度，移植代码时注意根据硬件情况调整正负
        angle = -(current_angle * math.pi) / 180
        # 计算摇杆旋转量
        temp = speed_y * math.cos(angle) + speed_x * math.sin(angle)
        speed_x = -1 * speed_y * math.sin(angle) + speed_x * math.cos(angle)
        speed_y = temp
        # SmartDashboard.putNumber("speed_x",(speed_x))
        # SmartDashboard.putNumber("speed_y",(speed_y))
        # print(f'speed_x={speed_x}')
        # print(f'speed_y={speed_y}')
        
        # 旋转停止后更新陀螺仪角度
        if speed_w == 0.0 and (not self.pre_speed_w == 0.0):
            self.target_angle_gyro = current_angle
        # 重新确定磁场定向驱动正方向
        if self.is_reset:
            self.is_reset = 0
            self.target_angle_gyro = current_angle
        # 更新角速度
        self.pre_speed_w = speed_w
        # 如果是直线模式，给出角速度修正量，以保证不自旋
        if speed_w == 0.0:
            speed_w = correct_yaw(self.target_angle_gyro, current_angle, current_angular_rate)
        if not is_dead_area:
            for i in range(4):
                # 记录上次速度
                self.wheel_lp[i].last_speed = self.wheel_lp[i].present_speed

        car_v = math.sqrt(speed_x ** 2 + speed_y ** 2)
        # 最大速度限制
        if car_v > self.SPEED_V_LIMIT:
            car_v = self.SPEED_V_LIMIT
        car_yaw = math.atan2(speed_y, speed_x)
        # SmartDashboard.putNumber('speedx',speed_x)
        # SmartDashboard.putNumber('speedy',speed_y)
        # SmartDashboard.putNumber('car_yaw',car_yaw)
        # 角度处理

        if car_yaw > math.pi * 0.5:
            car_yaw = car_yaw - math.pi
            car_v = -car_v
        if car_yaw < math.pi * -0.5:
            car_yaw = car_yaw + math.pi
            car_v = -car_v
        
        # SmartDashboard.putNumber("car_v",(car_v))
        # SmartDashboard.putNumber("car_yaw",(car_yaw))
        # print(f'car_v= {car_v}')
        # print(f'car_yaw= {car_yaw}')
        
        for i in range(4):
            self.wheel_lp[i].present_speed.m_vec_yaw = car_yaw
            self.wheel_lp[i].present_speed.m_vec_v = car_v

        if not speed_w == 0:
            # 速度赋值PTZ_yaw
            speed_w *=- 0.6  # 可更改,根据硬件调试
            self.wheel_info[0].m_vec_v = -speed_w
            self.wheel_info[1].m_vec_v = speed_w
            self.wheel_info[2].m_vec_v = -speed_w
            self.wheel_info[3].m_vec_v = speed_w

            # 计算轮子垂直向量坐标的角度朝向，在需要控制的云台坐标系中, use for circle self

            self.wheel_info[0].m_vec_yaw = self.PTZ_yaw - self.Circle_rad
            self.wheel_info[1].m_vec_yaw = self.PTZ_yaw + self.Circle_rad
            self.wheel_info[2].m_vec_yaw = self.PTZ_yaw + self.Circle_rad
            self.wheel_info[3].m_vec_yaw = self.PTZ_yaw - self.Circle_rad
            # 坐标系转换
            # 现在，车的移动方向是云台的方向
            for i in range(4):
                self.wheel_lp[i].present_speed.m_vec_yaw += self.PTZ_yaw
            # 分别在云台坐标系中直线与垂直向量相加得到和矢量，然后换算回电机坐标系
            for i in range(4):
                self.wheel_lp[i].present_speed = add_vectors(self.wheel_lp[i].present_speed, self.wheel_info[i])
                # 切换回电机yaw的坐标系
                self.wheel_lp[i].present_speed.m_vec_yaw = self.wheel_lp[i].present_speed.m_vec_yaw - self.PTZ_yaw

    def set_chassis_zero(self):
        for i in range(4):
            self.GIM_Wheel[i].set_target_angle_zero(0)

    def init_mega(self):
        self.gyro.clear_sticky_fault_bootup_gyroscope()
        self.gyro.set_yaw(0)
        self.is_reset = 1

    def chassis_init(self):
        # 舵轮底盘归零
        self.set_chassis_zero()
        # 初始化磁场定向控制，第三人称
        self.init_mega()
        # 初始化陀螺仪
        self.gyro_last_yaw = self.gyro.get_yaw()

    def run_speed(self, speed_scale, is_dead_area):
        for i in range(4):
            # 如果变换角度大于90°，反复循环直至小于90°
            while abs(self.wheel_lp[i].present_speed.m_vec_yaw - self.wheel_lp[i].last_speed.m_vec_yaw) > math.pi/2:
                if self.wheel_lp[i].present_speed.m_vec_yaw < self.wheel_lp[i].last_speed.m_vec_yaw:
                    self.wheel_lp[i].present_speed.m_vec_yaw += 2*math.pi
                else:
                    self.wheel_lp[i].present_speed.m_vec_yaw -= 2*math.pi
                self.wheel_lp[i].present_speed.m_vec_v = -self.wheel_lp[i].present_speed.m_vec_v
                # SmartDashboard.putNumber('present',self.wheel_lp[1].present_speed.m_vec_yaw * 180 / math.pi)
                # SmartDashboard.putNumber('last',self.wheel_lp[1].last_speed.m_vec_yaw * 180 / math.pi)
            if is_dead_area:
                self.GIM_Wheel[i].wheel_percent_ctrl(0)
                self.GIM_Wheel[i].set_target_angle(self.wheel_lp[i].last_speed.m_vec_yaw / (2 * math.pi))
            else:
                self.GIM_Wheel[i].wheel_percent_ctrl(speed_scale * self.wheel_lp[i].present_speed.m_vec_v)
                self.GIM_Wheel[i].set_target_angle(self.wheel_lp[i].present_speed.m_vec_yaw / (2 * math.pi))

    def fast_turn(self, target_angle_discrete_pov):
        if target_angle_discrete_pov == -1:
            return 0
        else:
            err = target_angle_discrete_pov - self.gyro.get_yaw().value_as_double
            err_time = self.gyro.get_angular_velocity_z_world().value_as_double
            while abs(err) > 180:
                if err > 180:
                    err -= 360
                if err < -180:
                    err += 360

            # 引入P控制，加限制幅值
            ans = - 0.0155 * err + 0.0015 * err_time
            return cap_filter(ans, 0.8)

    def fast_turn_abxy(self, abxy):
        if abxy == XboxController.A:
            return self.fast_turn(0)
        if abxy == XboxController.Y:
            return self.fast_turn(180)
        if abxy == XboxController.X:
            return self.fast_turn(90)
        if abxy == XboxController.B:
            return self.fast_turn(-90)
        if abxy == 270:
            return self.fast_turn(-120)
        if abxy == 90:
            return self.fast_turn(120)
        else:
            return 0
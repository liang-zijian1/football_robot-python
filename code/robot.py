import math
import wpilib
from phoenix6.hardware import Pigeon2,TalonFX,CANcoder
from phoenix6.controls import DutyCycleOut,PositionDutyCycle

class Chassis:
    def __init__(self):
        self.CAR_LENGTH = 0.5
        self.CAR_WIDTH = 0.5
        self.SPEED_V_LIMIT = 1.0
        self.SPEED_W_LIMIT = 1.0
        self.PI = math.pi

        self.Circle_rad = math.atan(self.CAR_LENGTH / self.CAR_WIDTH)
        self.car_V = 0.0
        self.car_yaw = 0.0

    def add_vectors(self, a, b):
        x = a['v'] * math.cos(a['yaw']) + b['v'] * math.cos(b['yaw'])
        y = a['v'] * math.sin(a['yaw']) + b['v'] * math.sin(b['yaw'])
        result_v = math.sqrt(x**2 + y**2)
        result_yaw = math.atan2(y, x)
        return {'v': result_v, 'yaw': result_yaw}

    def calc_speed(self, speed_x, speed_y, speed_w):
        car_V = math.sqrt(speed_x**2 + speed_y**2)
        car_yaw = math.atan2(speed_y, speed_x)

        if abs(car_yaw) > self.PI / 2:
            car_yaw = car_yaw - self.PI if car_yaw > 0 else car_yaw + self.PI
            car_V = -car_V

        car_yaw_rad = car_yaw

        # Calculate speed and direction for each wheel
        wheel_speeds = []
        for i in range(4):
            wheel_vector = {'v': car_V, 'yaw': car_yaw_rad}
            rotation_vector = {'v': speed_w, 'yaw': self.Circle_rad if i % 2 == 0 else -self.Circle_rad}
            combined_vector = self.add_vectors(wheel_vector, rotation_vector)
            wheel_speeds.append(combined_vector)

        return wheel_speeds

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # 在类里面声明对象
        self.chassis = Chassis()

        self.pigeon = Pigeon2(0)

        self.FL_drivemotor = TalonFX(1)
        self.FR_drivemotor = TalonFX(2)
        self.BR_drivemotor = TalonFX(3)
        self.BL_drivemotor = TalonFX(4)

        self.FL_steermotor = TalonFX(5)
        self.FR_steermotor = TalonFX(6)
        self.BR_steermotor = TalonFX(7)
        self.BL_steermotor = TalonFX(8)

        self.FL_cancoder = CANcoder(9)
        self.FR_cancoder = CANcoder(10)
        self.BR_cancoder = CANcoder(11)
        self.BL_cancoder = CANcoder(12)

        self.xbox_controller = wpilib.XboxController(0)
        
    def teleopPeriodic(self):
        left_x = self.xbox_controller.getLeftX()
        left_y = self.xbox_controller.getLeftY()
        right_x = self.xbox_controller.getRightX()
        yaw_angle = self.pigeon.get_yaw()
        
         # 如果需要磁场定向控制，可以对操纵杆输入进行坐标系转换
        angle_radians = math.radians(yaw_angle)#转弧度
        adjusted_left_x = left_x * math.cos(angle_radians) - left_y * math.sin(angle_radians)
        adjusted_left_y = left_x * math.sin(angle_radians) + left_y * math.cos(angle_radians)

        # 计算每个轮子的速度和方向
        wheel_speeds = self.chassis.calc_speed(adjusted_left_x, adjusted_left_y, right_x)
       
        # 使用CANcoder获取每个轮子的当前角度
        FL_current_angle = self.FL_cancoder.get_absolute_position()
        FR_current_angle = self.FR_cancoder.get_absolute_position()
        BR_current_angle = self.BR_cancoder.get_absolute_position()
        BL_current_angle = self.BL_cancoder.get_absolute_position()
        
        
        # 使用PID控制调整目标角度以减少误差
        FL_target_angle = self._calculate_target_angle(wheel_speeds[0]['yaw'], FL_current_angle)
        FR_target_angle = self._calculate_target_angle(wheel_speeds[1]['yaw'], FR_current_angle)
        BR_target_angle = self._calculate_target_angle(wheel_speeds[2]['yaw'], BR_current_angle)
        BL_target_angle = self._calculate_target_angle(wheel_speeds[3]['yaw'], BL_current_angle)
       
       # 设置每个轮子的速度和转向角度
        self.FL_drivemotor.set_control(DutyCycleOut(wheel_speeds[0]['v']))
        self.FR_drivemotor.set_control(DutyCycleOut(wheel_speeds[1]['v']))
        self.BR_drivemotor.set_control(DutyCycleOut(wheel_speeds[2]['v']))
        self.BL_drivemotor.set_control(DutyCycleOut(wheel_speeds[3]['v']))

        self.FL_steermotor.set_control(PositionDutyCycle(FL_target_angle))
        self.FR_steermotor.set_control(PositionDutyCycle(FR_target_angle))
        self.BR_steermotor.set_control(PositionDutyCycle(BR_target_angle))
        self.BL_steermotor.set_control(PositionDutyCycle(BL_target_angle))
        
    def _calculate_target_angle(self, desired_yaw, current_yaw):
        
        #计算目标角度与当前角度之间的最小旋转量，并调整方向。
        
        error = desired_yaw - current_yaw
        
        # 处理超过360度的情况，保持在 [-180, 180] 范围内
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360

        # 返回修正后的目标角度
        return current_yaw + error
import wpilib
import math
from wpilib import XboxController
from phoenix6.hardware import TalonFX, CANcoder,Pigeon2
from phoenix6.controls import DutyCycleOut, PositionDutyCycle
from phoenix5 import TalonSRX

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

        # 为每个轮子计算速度和方向
        wheel_speeds = []
        for i in range(4):
            wheel_vector = {'v': car_V, 'yaw': car_yaw_rad}
            rotation_vector = {'v': speed_w, 'yaw': self.Circle_rad if i % 2 == 0 else -self.Circle_rad}
            combined_vector = self.add_vectors(wheel_vector, rotation_vector)
            wheel_speeds.append(combined_vector)

        return wheel_speeds

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        # 初始化驱动和转向电机
        self.FL_drive_motor = TalonFX(1)  
        self.FL_steer_motor = TalonFX(2)  
        self.FR_drive_motor = TalonFX(4)
        self.FR_steer_motor = TalonFX(5)
        self.BL_drive_motor = TalonFX(7)
        self.BL_steer_motor = TalonFX(8)
        self.BR_drive_motor = TalonFX(10)
        self.BR_steer_motor = TalonFX(11)
        #初始化上层电机
        self.yaw_motor = TalonSRX(13)
       
        # 初始化 CANcoder 编码器
        self.FL_CANcoder = CANcoder(3)  
        self.FR_CANcoder = CANcoder(6)
        self.BL_Magcoder = TalonSRX(9)
        self.BR_CANcoder = CANcoder(12)
        
        
        #初始化陀螺仪
        self.pigeon = Pigeon2(0)
        
        # 初始化 Xbox 手柄
        self.controller = XboxController(0)
       
    def teleopInit(self) -> None:
        # cancoder的0位置
        FL_cancoder_offset=0.310791
        FR_cancoder_offset=0.041016
        BL_Magcoder_offset=0
        BR_cancoder_offset=-0.437012
       
        #获取电机当前位置
        self.left_front_steer_motor_postion=self.FL_steer_motor.get_position().value_as_double
        self.right_front_steer_motor_postion=self.FR_steer_motor.get_position().value_as_double
        self.left_back_steer_motor_position=self.BL_steer_motor.get_position().value_as_double
        self.right_back_steer_motor_postion=self.BR_steer_motor.get_position().value_as_double
        
       
        # 计算实际角度与0位置的误差
        FL_cancoder_real_angle=self.FL_CANcoder.get_absolute_position().value_as_double
        self.left_front_error=-FL_cancoder_real_angle+FL_cancoder_offset
        
        FR_cancoder_real_angle=self.FR_CANcoder.get_absolute_position().value_as_double
        self.right_front_error=-FR_cancoder_real_angle+FR_cancoder_offset
        
        BL_Magcoder_real_angle=self.BL_Magcoder.getSelectedSensorPosition()
        self.left_back_error=-BL_Magcoder_real_angle+BL_Magcoder_offset
        
        BR_cancoder_real_angle=self.BR_CANcoder.get_absolute_position().value_as_double
        self.right_back_error=-BR_cancoder_real_angle+BR_cancoder_offset
        
        #设置舵向回中
        self.FL_steer_motor.set_control(PositionDutyCycle(self.left_front_error*12.84375+self.left_front_steer_motor_postion))
        self.FR_steer_motor.set_control(PositionDutyCycle(self.right_front_error*12.84375+self.right_front_steer_motor_postion))
        self.BR_steer_motor.set_control(PositionDutyCycle(self.right_back_error*12.84375+self.right_back_steer_motor_postion))
        
        self.wheel_init_offset_FL=self.left_front_error*12.84375+self.left_front_steer_motor_postion
        self.wheel_init_offset_FR=self.right_front_error*12.84375+self.right_front_steer_motor_postion
        self.wheel_init_offset_BR=self.right_back_error*12.84375+self.right_back_steer_motor_postion
        
        return super().teleopInit()
        
    def teleopPeriodic(self):
        # 读取手柄左摇杆的 X 和 Y 值，右摇杆的X值
        left_x = self.controller.getLeftX()
        left_y = self.controller.getLeftY()
        right_x = self.controller.getRightX()
        yaw_angle = self.pigeon.get_yaw().value_as_double
        #死区检测 
        if math.sqrt(left_x ** 2 + left_y ** 2) >0.1 :
            x_input_ture=left_x
            y_input_ture=left_y
        else:
            x_input_ture=0
            y_input_ture=0
            self.FL_steer_motor.set_control(PositionDutyCycle(self.left_front_error*12.84375+self.left_front_steer_motor_postion))
            self.FR_steer_motor.set_control(PositionDutyCycle(self.right_front_error*12.84375+self.right_front_steer_motor_postion))
            self.BR_steer_motor.set_control(PositionDutyCycle(self.right_back_error*12.84375+self.right_back_steer_motor_postion))
        
        if right_x>0.2:
            w=right_x
        else:
            w=0
       
        # 如果需要磁场定向控制，可以对操纵杆输入进行坐标系转换
        angle_radians = math.radians(yaw_angle)#转弧度
        adjusted_left_x = x_input_ture * math.cos(angle_radians) - y_input_ture * math.sin(angle_radians)#从地面坐标系转到机器人坐标
        adjusted_left_y = x_input_ture * math.sin(angle_radians) + y_input_ture * math.cos(angle_radians)#从地面坐标系转到机器人坐标

        # 计算每个轮子的速度和方向
        wheel_speeds =self.chassis.calc_speed(adjusted_left_x, adjusted_left_y, w)
       
        # 获取当前的转向角度
        current_angle = self.FL_steer_motor.get_position().value_as_double
        
        # print(left_front_error)

        # 将速度发送给驱动电机
        self.FL_drive_motor.set_control(DutyCycleOut(wheel_speeds[0]['v']*0.15))
        self.FR_drive_motor.set_control(DutyCycleOut(wheel_speeds[1]['v']*0.15))
        self.BR_drive_motor.set_control(DutyCycleOut(wheel_speeds[2]['v']*0.15))
        self.BL_drive_motor.set_control(DutyCycleOut(wheel_speeds[3]['v']*0.15))
        #print(wheel_speeds)
        # 将目标角度发送给转向电机
        self.FL_steer_motor.set_control(PositionDutyCycle(self.wheel_init_offset_FL-wheel_speeds[0]['yaw']/(2*3.1415926)*12.84375))
        #self.FR_steer_motor.set_control(PositionDutyCycle(self.wheel_init_offset_FL+wheel_speeds[1]['yaw']/(2*3.1415926)*12.84375))
        #self.BR_steer_motor.set_control(PositionDutyCycle(self.wheel_init_offset_FL+wheel_speeds[2]['yaw']/(2*3.1415926)*12.84375))

        
    
if __name__ == "__main__":
    wpilib.run(MyRobot)

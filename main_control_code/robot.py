#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#
# import wpilib.drive  # Used for the DifferentialDrive class
# from phoenix6.hardware import Pigeon2, TalonFX, CANcoder
# from phoenix6.controls import DutyCycleOut, TorqueCurrentFOC, VoltageOut, PositionDutyCycle, PositionVoltage, PositionTorqueCurrentFOC, VelocityDutyCycle, VelocityVoltage, VelocityTorqueCurrentFOC, MotionMagicDutyCycle, MotionMagicVoltage, MotionMagicTorqueCurrentFOC, DifferentialDutyCycle, DifferentialVoltage, DifferentialPositionDutyCycle, DifferentialPositionVoltage, DifferentialVelocityDutyCycle, DifferentialVelocityVoltage, DifferentialMotionMagicDutyCycle, DifferentialMotionMagicVoltage, Follower, StrictFollower, DifferentialFollower, DifferentialStrictFollower, NeutralOut, CoastOut, StaticBrake, MusicTone, MotionMagicVelocityDutyCycle, MotionMagicVelocityTorqueCurrentFOC, MotionMagicVelocityVoltage, MotionMagicExpoDutyCycle, MotionMagicExpoVoltage, MotionMagicExpoTorqueCurrentFOC, DynamicMotionMagicDutyCycle, DynamicMotionMagicVoltage, DynamicMotionMagicTorqueCurrentFOC
# from phoenix5 import TalonSRX, ControlMode,VictorSPX,VictorSPXControlMode
# from wpilib import XboxController
# from wpilib import SmartDashboard
# from wpilib import AddressableLED
# import math
import wpilib
from ballpipe import Ballpipe
from chassis import Chassis,Helper,non_leaner_control
from led import LED
from pitch import Pitch
from roll import Roll
from shooter import Shooter
from yaw import Yaw

#from networktables import NetworkTable
#from chassis import Speed,SpeedT,add_vectors, non_leaner_control,Vec3d, Wheel,Helper,Chassis

# import time
# import Chassis
# class Speed:
#     def __init__(self, vec_v, vec_yaw):
#         self.m_vec_v = vec_v
#         self.m_vec_yaw = vec_yaw


# class SpeedT:
#     def __init__(self):
#         self.last_speed = Speed(0, 0)
#         self.present_speed = Speed(0, 0)


# def add_vectors(a, b):
#     x = a.m_vec_v * math.cos(a.m_vec_yaw) + b.m_vec_v * math.cos(b.m_vec_yaw)
#     y = a.m_vec_v * math.sin(a.m_vec_yaw) + b.m_vec_v * math.sin(b.m_vec_yaw)
#     result_v = math.sqrt(x ** 2 + y ** 2)
#     result_yaw = math.atan2(y, x)
#     return Speed(result_v, result_yaw)


# def non_leaner_control(inputs):
#     inputs = 0.31083769050760857 * math.sinh(0.5859152429745125 * math.sinh(1.8849555921538759 * inputs))
#     return inputs


# class Vec3d:
#     def __init__(self):
#         self.x = 0
#         self.y = 0
#         self.w = 0


# class Wheel:
#     def __init__(self, drive_id, servo_id, coder_id, offset):
#         self.m_offset = offset
#         self.servo_gear = 12.84375
#         self.offset_inter = 0
#         self.drive_motor = TalonFX(drive_id)
#         self.servo_motor = TalonFX(servo_id)
#         self.servo_coder = CANcoder(coder_id)

#     def set_target_angle_zero(self, rotation):
#         err_rota = rotation + self.servo_coder.get_absolute_position().value_as_double - self.m_offset
#         target = self.servo_motor.get_position().value_as_double - err_rota * self.servo_gear
#         self.servo_motor.set_control(PositionDutyCycle(target))
#         self.offset_inter = target
#         # SmartDashboard.putNumber("target", target)

#     def set_target_angle(self, rotation):
#         rotation = rotation * self.servo_gear
#         self.servo_motor.set_control(PositionDutyCycle(rotation + self.offset_inter))

#     def wheel_percent_ctrl(self, percent):
#         self.drive_motor.set_control(DutyCycleOut(percent))


# class Helper:
#     def __init__(self):
#         self.is_dead_band = True

#     def death_judge(self, n, m, p_uni):
#         temp = Vec3d()
#         if (n ** 2 + m ** 2 > 0.1 ** 2) or abs(p_uni) > 0.1:
#             if n ** 2 + m ** 2 > 0.1 ** 2:
#                 temp.x = n
#                 temp.y = m
#             else:
#                 temp.x = 0
#                 temp.y = 0
#             if abs(p_uni) > 0.1:
#                 temp.w = p_uni
#             else:
#                 temp.w = 0
#             self.is_dead_band = False
#             return temp
#         else:
#             temp.x = 0
#             temp.y = 0
#             temp.w = 0
#             self.is_dead_band = True
#             return temp

#     def get_dead_band(self):
#         return self.is_dead_band


# def dead_bond_filter(axis_val):
#     if 0.06 > axis_val > -0.06:
#         axis_val = 0
#     return axis_val


# def cap_filter(value, peak):
#     if value < -peak:
#         return -peak
#     if value > +peak:
#         return +peak
#     return value


# def correct_yaw(_target_angle_gyro, _current_angle, _current_angular_rate):
#     # grab some input data from Pigeon and gamepad
#     rcw_error = (_target_angle_gyro - _current_angle) * (-0.009) - _current_angular_rate * (-0.001)  # PD没有I control
#     rcw_error = cap_filter(rcw_error, 0.75)
#     rcw_error = dead_bond_filter(rcw_error)
#     return rcw_error


# class Chassis:
#     def __init__(self):
#         # 车辆固有属性
#         self.CAR_LENGTH = 0.5
#         self.CAR_WIDTH = 0.5
#         self.SPEED_V_LIMIT = 1.0
#         self.SPEED_W_LIMIT = 1.0

#         self.Circle_rad = math.atan(self.CAR_LENGTH / self.CAR_WIDTH)

#         # 车辆状态变量
#         self.car_V = 0.0
#         self.car_yaw = 0.0
#         self.PTZ_yaw = 0.0
#         self.pre_speed_w = 0.0
#         self.target_angle_gyro = 0.0
#         self.gyro_last_yaw = 0.0
#         self.is_reset = 0

#         # 轮组状态变量
#         self.wheel_speeds = [Speed(0, 0), Speed(0, 0), Speed(0, 0), Speed(0, 0)]
#         self.wheel_lp = [SpeedT(), SpeedT(), SpeedT(), SpeedT()]
#         self.wheel_info = [Speed(0, 0), Speed(0, 0), Speed(0, 0), Speed(0, 0)]

#         # 轮组硬件属性及硬件声明
#         wheel_data = [
#             (1, 2, 3, 0.316162),  # FL
#             (4, 5, 6, -0.467285),  # FR
#             (7, 8, 9, -0.118652),  # BL
#             (10, 11, 12, 0.313721)  # BR
#         ]
#         self.GIM_Wheel = [Wheel(drive_id, servo_id, coder_id, offset) for drive_id, servo_id, coder_id, offset in
#                           wheel_data]
#         self.gyro = Pigeon2(0)

#     def calc_speed(self, speed_x, speed_y, speed_w, is_dead_area):
#         current_angle = self.gyro.get_yaw().value_as_double - 90  # remain bug,得到deg
#         # print(self.gyro.get_yaw().value_as_double)
#         # 得到角度变化率，用于PID的D参数
#         current_angular_rate = self.gyro.get_angular_velocity_z_world().value_as_double  # remain bug
#         # print(current_angular_rate)
#         # 将角度转化为弧度，移植代码时注意根据硬件情况调整正负
#         angle = +(current_angle * math.pi) / 180
#         # 计算摇杆旋转量
#         temp = speed_y * math.cos(angle) + speed_x * math.sin(angle)
#         speed_x = -1 * speed_y * math.sin(angle) + speed_x * math.cos(angle)
#         speed_y = temp
#         # 旋转停止后更新陀螺仪角度
#         if speed_w == 0.0 and (not self.pre_speed_w == 0.0):
#             self.target_angle_gyro = current_angle
#         # 重新确定磁场定向驱动正方向
#         if self.is_reset:
#             self.is_reset = 0
#             self.target_angle_gyro = current_angle
#         # 更新角速度
#         self.pre_speed_w = speed_w
#         # 如果是直线模式，给出角速度修正量，以保证不自旋
#         if speed_w == 0.0:
#             speed_w = correct_yaw(self.target_angle_gyro, current_angle, current_angular_rate)
#         if not is_dead_area:
#             for i in range(4):
#                 # 记录上次速度
#                 self.wheel_lp[i].last_speed = self.wheel_lp[i].present_speed

#         car_v = math.sqrt(speed_x ** 2 + speed_y ** 2)
#         # 最大速度限制
#         if car_v > self.SPEED_V_LIMIT:
#             car_v = self.SPEED_V_LIMIT
#         car_yaw = math.atan2(speed_y, speed_x)
#         # 角度处理
#         if abs(car_yaw > math.pi * 0.5):
#             car_yaw = car_yaw - math.pi
#             car_v = -car_v
#         if abs(car_yaw < math.pi * -0.5):
#             car_yaw = car_yaw + math.pi
#             car_v = -car_v

#         for i in range(4):
#             self.wheel_lp[i].present_speed.m_vec_yaw = car_yaw
#             self.wheel_lp[i].present_speed.m_vec_v = car_v

#         if not speed_w == 0:
#             # 速度赋值PTZ_yaw
#             speed_w *= 0.6  # 可更改
#             self.wheel_info[0].m_vec_v = -speed_w
#             self.wheel_info[1].m_vec_v = speed_w
#             self.wheel_info[2].m_vec_v = -speed_w
#             self.wheel_info[3].m_vec_v = speed_w

#             # 计算轮子垂直向量坐标的角度朝向，在需要控制的云台坐标系中, use for circle self

#             self.wheel_info[0].m_vec_yaw = self.PTZ_yaw - self.Circle_rad
#             self.wheel_info[1].m_vec_yaw = self.PTZ_yaw + self.Circle_rad
#             self.wheel_info[2].m_vec_yaw = self.PTZ_yaw + self.Circle_rad
#             self.wheel_info[3].m_vec_yaw = self.PTZ_yaw - self.Circle_rad
#             # 坐标系转换
#             # 现在，车的移动方向是云台的方向
#             for i in range(4):
#                 self.wheel_lp[i].present_speed.m_vec_yaw += self.PTZ_yaw
#             # 分别在云台坐标系中直线与垂直向量相加得到和矢量，然后换算回电机坐标系
#             for i in range(4):
#                 self.wheel_lp[i].present_speed = add_vectors(self.wheel_lp[i].present_speed, self.wheel_info[i])
#                 # 切换回电机yaw的坐标系
#                 self.wheel_lp[i].present_speed.m_vec_yaw = self.wheel_lp[i].present_speed.m_vec_yaw - self.PTZ_yaw

#     def set_chassis_zero(self):
#         for i in range(4):
#             self.GIM_Wheel[i].set_target_angle_zero(0)

#     def init_mega(self):
#         self.gyro.clear_sticky_fault_bootup_gyroscope()
#         self.is_reset = 1

#     def chassis_init(self):
#         # 舵轮底盘归零
#         self.set_chassis_zero()
#         # 初始化磁场定向控制，第三人称
#         self.init_mega()
#         # 初始化陀螺仪
#         self.gyro_last_yaw = self.gyro.get_yaw()

#     def run_speed(self, speed_scale, is_dead_area):
#         for i in range(4):
#             # 如果变换角度大于90°，反复循环直至小于90°

#             while abs(self.wheel_lp[i].present_speed.m_vec_yaw - self.wheel_lp[i].last_speed.m_vec_yaw) > math.pi * 0.5:
#                 if self.wheel_lp[i].present_speed.m_vec_yaw < self.wheel_lp[i].last_speed.m_vec_yaw:
#                     self.wheel_lp[i].present_speed.m_vec_yaw += math.pi
#                 else:
#                     self.wheel_lp[i].present_speed.m_vec_yaw -= math.pi
#                 self.wheel_lp[i].present_speed.m_vec_v = -self.wheel_lp[i].present_speed.m_vec_v
#             # print(self.wheel_lp[1].present_speed.m_vec_yaw * 180 / math.pi)
#             if is_dead_area:
#                 self.GIM_Wheel[i].wheel_percent_ctrl(0)
#                 self.GIM_Wheel[i].set_target_angle(self.wheel_lp[i].last_speed.m_vec_yaw / (2 * math.pi))
#             else:
#                 self.GIM_Wheel[i].wheel_percent_ctrl(speed_scale * self.wheel_lp[i].present_speed.m_vec_v)
#                 self.GIM_Wheel[i].set_target_angle(self.wheel_lp[i].present_speed.m_vec_yaw / (2 * math.pi))

#     def fast_turn(self, target_angle_discrete_pov):
#         if target_angle_discrete_pov == -1:
#             return 0
#         else:
#             err = target_angle_discrete_pov - self.gyro.get_yaw().value_as_double
#             err_time = self.gyro.get_angular_velocity_z_world().value_as_double
#             while abs(err) > 180:
#                 if err > 180:
#                     err -= 360
#                 if err < -180:
#                     err += 360

#             # 引入P控制，加限制幅值
#             ans = - 0.0155 * err + 0.0015 * err_time
#             return cap_filter(ans, 0.8)

#     def fast_turn_abxy(self, abxy):
#         if abxy == XboxController.A:
#             return self.fast_turn(0)
#         if abxy == XboxController.Y:
#             return self.fast_turn(180)
#         if abxy == XboxController.X:
#             return self.fast_turn(90)
#         if abxy == XboxController.B:
#             return self.fast_turn(-90)
#         if abxy == 270:
#             return self.fast_turn(-120)
#         if abxy == 90:
#             return self.fast_turn(120)
#         else:
#             return 0


# # class FrcInstrument:
# #     def __init__(self):
# #         tone1 = TalonFX(1)
# #         tone2 = TalonFX(2)
# #         tone3 = TalonFX(5)
# class Yaw:
#     def __init__(self):
#         self.position2 = None
#         self.position1 = None
#         self.p_position_units = None
#         self.yaw_motor = TalonSRX(13)
#         self.middle_position = 2393  # units
#         self.step = 20  # units

#     def init_motor(self):
#         self.yaw_motor.set(ControlMode.Position, self.middle_position)

#     def control(self, button1, button2):
#         self.p_position_units = self.yaw_motor.getSelectedSensorPosition()
#         # self.p_position_deg = self.p_position_units/4096*360
#         if 1870 < self.p_position_units < 2900:
#             if button1:
#                 self.position1 = self.yaw_motor.getSelectedSensorPosition()
#                 self.yaw_motor.set(ControlMode.Position, self.position1 + self.step)
#                 # SmartDashboard.putNumber("sb1",90-((self.position1+self.step-self.middle_position)/4096*360))
#             if button2:
#                 self.position2 = self.yaw_motor.getSelectedSensorPosition()
#                 self.yaw_motor.set(ControlMode.Position, self.position2 - self.step)
#                 # SmartDashboard.putNumber("sb2",90+((self.position2-self.step-self.middle_position)/4096*360))
#             SmartDashboard.putNumber("Yaw Angle(deg)",
#                                      90 + ((self.p_position_units - self.middle_position) / 4096 * 360))
#         else:
#             self.yaw_motor.set(ControlMode.Position, self.middle_position)


# class Pitch:
#     def __init__(self):
#         self.pitch_p_position_deg = None
#         self.pitch_position2 = None
#         self.pitch_position1 = None
#         self.pitch_p_position_units = None
#         self.pitch_motor1 = TalonSRX(15)
#         self.pitch_motor2 = TalonSRX(16)
#         self.pitch_max_position = 500  # units,最低点
#         self.pitch_min_position = 23
#         self.pitch_step =  30 # units

#     def motor_init(self):
#         self.pitch_motor1.set(ControlMode.Position, 350)
#         self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())

#     def control(self, pitch_button1, pitch_button2):
#         self.pitch_p_position_units = self.pitch_motor1.getSelectedSensorPosition()
#         #print(self.pitch_p_position_units)
#         # self.pitch_p_position_deg = self.pitch_p_position_units / 4096 * 360
#         if 20 < self.pitch_p_position_units < 510:
#             if pitch_button1:
#                 self.pitch_position1 = self.pitch_motor1.getSelectedSensorPosition()
#                 self.pitch_motor1.set(ControlMode.Position, self.pitch_position1 - self.pitch_step)
#                 self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())
#                 # SmartDashboard.putNumber("sb1",90-((self.position1+self.step-self.middle_position)/4096*360))
#             if pitch_button2:
#                 self.pitch_position2 = self.pitch_motor1.getSelectedSensorPosition()
#                 self.pitch_motor1.set(ControlMode.Position, self.pitch_position2 + self.pitch_step)
#                 self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())
#                 # SmartDashboard.putNumber("sb2",90+((self.position2-self.step-self.middle_position)/4096*360))
#             SmartDashboard.putNumber("Pitch Angle(deg)", (self.pitch_p_position_units-23) / 4096 * 360)
#         else:
#             self.pitch_motor1.set(ControlMode.Position, 350)
#             self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())

# class Roll:
#     def __init__(self):
#         self.roll_motor = TalonFX(14)
#         self.dio_input = wpilib.DigitalInput(9)
#         self.init_position = None
#         self.init_step = 0.505527
#         self.is_initialized = False

#     def init_motor(self):
#         # 每次重新启用时手动调用
#         self.is_initialized = False  # 每次重新启用时重置

#     def periodic_motor_control(self,pov):
#         # 在teleopPeriodic中持续调用
#         dio_state = self.dio_input.get()
#         if dio_state == False and not self.is_initialized:
#             self.init_position = self.roll_motor.get_position().value_as_double
#             self.roll_motor.set_control(PositionDutyCycle(self.init_position - self.init_step))
#             self.is_initialized = True  # 标记已归中
#         elif not self.is_initialized:
#             # 如果尚未归中，继续转动电机直到检测到 False
#             self.roll_motor.set_control(DutyCycleOut(0.046))
#         else:
#             # 电机已归中，可以进行其他操作
#             if pov==90:
#                 self.roll_motor.set_control(PositionDutyCycle(self.init_position))
#             if pov==270:
#                 self.roll_motor.set_control(PositionDutyCycle(self.init_position-self.init_step*2))
#             if pov==0:
#                 self.roll_motor.set_control(PositionDutyCycle(self.init_position - self.init_step))
# class Shooter: 
    
#     def __init__(self):
#         self.shooter_left=TalonFX(17)
#         self.shooter_right=TalonFX(18)
#         self.target_velocity_left=-50
#         self.target_velocity_right=40
    
#     def control(self, button1, button2,):
#         if button1 > 0.1 or button2 > 0.1:
#             # 正转和反转设定
#             self.shooter_left.set_control(VelocityDutyCycle(velocity=self.target_velocity_left,acceleration=-2.0,feed_forward=-0.2,enable_foc=True,slot=0))
#             self.shooter_right.set_control(VelocityDutyCycle(velocity=self.target_velocity_right,acceleration=2.0,feed_forward=0.2,enable_foc=True,slot=0))
#         else:
#             # 低速保持
#             self.shooter_left.set_control(VelocityDutyCycle(velocity=-5, feed_forward=-0.2,slot=1))
#             self.shooter_right.set_control(VelocityDutyCycle(velocity=5, feed_forward=0.2,slot=1))
        
#         # 输出到 SmartDashboard
#         self.left_velocity = self.shooter_left.get_velocity().value_as_double
#         self.right_velocity = self.shooter_right.get_velocity().value_as_double
#         SmartDashboard.putNumber("average_velocity", (self.left_velocity + self.right_velocity) * 0.5)
#         SmartDashboard.putNumber("velocity_difference", abs(self.left_velocity - self.right_velocity))
       
# class Ballpipe:
#     def __init__(self):
#         self.Ballpipe_motor = VictorSPX(2)
        
#     def control(self,button):
#         if button==True:
#             self.Ballpipe_motor.set(VictorSPXControlMode.PercentOutput, -1)
#         else:
#             self.Ballpipe_motor.set(VictorSPXControlMode.PercentOutput, 0)
# class LED:
#     def __init__(self):
#         if not hasattr(self, 'led'):
#             self.led = AddressableLED(0)  # 使用PWM端口0
#             self.led_buffer = [AddressableLED.LEDData(0, 0, 0) for _ in range(60)]  
#             self.led.setLength(len(self.led_buffer))
#             self.led.setData(self.led_buffer)
#             self.led.start()
#             self.blink_state = False
#             self.counter = 0
      
#     def set_color(self, r: int, g: int, b: int, brightness: float = 1.0):
#         """设置所有LED的颜色并调节亮度"""
#         r = int(r * brightness)
#         g = int(g * brightness)
#         b = int(b * brightness)
    
#         for i in range(len(self.led_buffer)):
#             self.led_buffer[i].setRGB(r, g, b)
#         self.led.setData(self.led_buffer)
    
#     def blink(self,r: int, g: int, b: int, brightness: float = 1.0):
#         """控制LED闪烁"""
#         self.counter += 1
#         if self.counter % 10 == 0:  # 控制闪烁频率
#             self.blink_state = not self.blink_state
#             if self.blink_state:
#                 self.set_color(r* brightness,g* brightness,b* brightness)  # 开启绿色
#             else:
#                 self.set_color(0, 0, 0)  # 关闭
  
class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.controller = wpilib.XboxController(0)
        self.my_chassis = Chassis()
        self.helper = Helper()
        self.my_Yaw = Yaw()
        self.my_Pitch = Pitch()
        self.my_Roll = Roll()
        self.my_Shooter = Shooter()
        self.my_ballpipe = Ballpipe()
        self.my_led = LED()
        self.my_led.set_color(255,0,0)
    
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        # self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        #
        # # Drive for two seconds
        # if self.timer.get() < 2.0:
        #     # Drive forwards half speed, make sure to turn input squaring off
        #     self.robotDrive.arcadeDrive(0.5, 0, squareInputs=False)
        # else:
        #     self.robotDrive.stopMotor()  # Stop robot

    def teleopInit(self):
        self.my_chassis.chassis_init()
        self.my_Yaw.init_motor()
        self.my_Pitch.motor_init()
        self.my_Roll.init_motor()
        self.my_led.set_color(0, 255, 0,brightness=0.25) 

    def teleopPeriodic(self):
        self.my_chassis.calc_speed(
            non_leaner_control(
                self.helper.death_judge(-self.controller.getLeftX(), self.controller.getLeftY(),
                                        self.controller.getRightX()).x),
            non_leaner_control(
                self.helper.death_judge(-self.controller.getLeftX(), self.controller.getLeftY(),
                                        self.controller.getRightX()).y),
            non_leaner_control(
                self.helper.death_judge(-self.controller.getLeftX(), self.controller.getLeftY(),
                                        self.controller.getRightX()).w),
            self.helper.get_dead_band())
        self.my_chassis.run_speed(0.5, self.helper.get_dead_band())
        self.my_Yaw.control(self.controller.getBButtonPressed(), self.controller.getAButtonPressed())
        self.my_Pitch.control(self.controller.getXButtonPressed(), self.controller.getYButtonPressed())
        self.my_Shooter.control(self.controller.getRightTriggerAxis(), self.controller.getLeftTriggerAxis())
        self.my_Roll.periodic_motor_control(self.controller.getPOV()) 
        self.my_ballpipe.control(self.controller.getRightBumper())
        if abs(self.my_Shooter.left_velocity - self.my_Shooter.target_velocity_left) < 2 and abs(self.my_Shooter.right_velocity - self.my_Shooter.target_velocity_right) < 2:
            self.my_led.blink(0, 255, 0)  # 绿灯闪烁表示速度平稳可以射球
        else:    
            self.my_led.set_color(0,255,0,brightness=0.25)
       


    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        
    def disabledInit(self):
        self.my_led.set_color(255,0,0,brightness=0.25)

if __name__ == "__main__":
    wpilib.run(MyRobot)

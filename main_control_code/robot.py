#!/usr/bin/env python3.12
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from ballpipe import Ballpipe
from chassis import Chassis,Helper,non_leaner_control
from led import LED
from pitch import Pitch
from roll import Roll
from shooter import Shooter
from yaw import Yaw
from networktables import NetworkTables
from autoaim import AutoAim
import logging

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
        # 初始化 NetworkTables 服务器（RoboRIO 作为服务器）
        logging.basicConfig(level=logging.DEBUG)
        NetworkTables.initialize(server='10.2.54.2')
        # 获取 'SmartDashboard' 表
        self.table = NetworkTables.getTable('SmartDashboard')
        
        # 自瞄实例
        self.auto_aim = AutoAim(self.my_Yaw, self.my_Pitch, self.controller, self.table)
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
        self.my_led.set_color(0, 255, 0,brightness=0.15) 

    def teleopPeriodic(self):
        if self.controller.getStartButtonPressed():
            self.my_chassis.init_mega()
        
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
        # 自瞄控制
        self.auto_aim.toggle_aiming_mode()
        
        #print("All keys in NetworkTables:", self.table.getKeys())
        
        if self.auto_aim.aiming_mode:
            self.my_led.set_color(128, 0, 128)  # 紫色闪烁表示进入自瞄模式
            self.auto_aim.auto_aim()  # 执行自瞄逻辑
        else:
        
            if abs(self.my_Shooter.left_velocity - self.my_Shooter.target_velocity_left) < 2 and abs(self.my_Shooter.right_velocity - self.my_Shooter.target_velocity_right) < 2:
                self.my_led.blink(0, 255, 0,brightness=0.15)  # 绿灯闪烁表示速度平稳可以射球
            else:    
                self.my_led.set_color(0,255,0,brightness=0.15)
       
    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        
    def disabledInit(self):
        self.my_led.set_color(255,0,0,brightness=0.15)


if __name__ == "__main__":
    wpilib.run(MyRobot)

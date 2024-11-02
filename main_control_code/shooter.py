from phoenix6.hardware import TalonFX
from phoenix6.controls import VelocityDutyCycle
from wpilib import SmartDashboard
import math

class Shooter: 
    def __init__(self):
        self.shooter_left = TalonFX(17)
        self.shooter_right = TalonFX(18)
        
        # 初始化目标速度
        self.target_velocity_left = -40
        self.target_velocity_right = 40

        # 将初始目标速度值推送到 SmartDashboard 上
        SmartDashboard.putNumber("Target Velocity Left", self.target_velocity_left)
        SmartDashboard.putNumber("Target Velocity Right", self.target_velocity_right)
    
    def control(self, button1, button2):
        # 从 SmartDashboard 获取更新后的目标速度
        self.target_velocity_left = SmartDashboard.getNumber("Target Velocity Left", self.target_velocity_left)
        self.target_velocity_right = SmartDashboard.getNumber("Target Velocity Right", self.target_velocity_right)
        
        if button1 > 0.1 or button2 > 0.1:
            # 正转和反转设定
            self.shooter_left.set_control(VelocityDutyCycle(
                velocity=self.target_velocity_left,
                acceleration=-2.0,
                feed_forward=-0.2,
                enable_foc=True,
                slot=0
            ))
            self.shooter_right.set_control(VelocityDutyCycle(
                velocity=self.target_velocity_right,
                acceleration=2.0,
                feed_forward=0.2,
                enable_foc=True,
                slot=0
            ))
        else:
            # 低速保持
            self.shooter_left.set_control(VelocityDutyCycle(velocity=-8, feed_forward=-0.2, slot=1))
            self.shooter_right.set_control(VelocityDutyCycle(velocity=8, feed_forward=0.2, slot=0))
        
        # 输出到 SmartDashboard
        self.left_velocity = self.shooter_left.get_velocity().value_as_double
        self.right_velocity = self.shooter_right.get_velocity().value_as_double
        SmartDashboard.putNumber("Left Velocity", self.left_velocity)
        SmartDashboard.putNumber("Right Velocity", self.right_velocity)
        SmartDashboard.putNumber("Average Velocity", abs(self.left_velocity - self.right_velocity) * 0.5 )
        SmartDashboard.putNumber("Velocity Difference", abs(self.left_velocity + self.right_velocity))

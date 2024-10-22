from phoenix6.hardware import TalonFX
from phoenix6.controls import VelocityDutyCycle
from wpilib import SmartDashboard
class Shooter: 
    
    def __init__(self):
        self.shooter_left=TalonFX(17)
        self.shooter_right=TalonFX(18)
        self.target_velocity_left=-50
        self.target_velocity_right=40
    
    def control(self, button1, button2,):
        if button1 > 0.1 or button2 > 0.1:
            # 正转和反转设定
            self.shooter_left.set_control(VelocityDutyCycle(velocity=self.target_velocity_left,acceleration=-2.0,feed_forward=-0.2,enable_foc=True,slot=0))
            self.shooter_right.set_control(VelocityDutyCycle(velocity=self.target_velocity_right,acceleration=2.0,feed_forward=0.2,enable_foc=True,slot=0))
        else:
            # 低速保持
            self.shooter_left.set_control(VelocityDutyCycle(velocity=-6, feed_forward=-0.2,slot=1))
            self.shooter_right.set_control(VelocityDutyCycle(velocity=6, feed_forward=0.2,slot=1))
        
        # 输出到 SmartDashboard
        self.left_velocity = self.shooter_left.get_velocity().value_as_double
        self.right_velocity = self.shooter_right.get_velocity().value_as_double
        SmartDashboard.putNumber("average_velocity", (self.left_velocity + self.right_velocity) * 0.5)
        SmartDashboard.putNumber("velocity_difference", abs(self.left_velocity - self.right_velocity))
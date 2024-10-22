from phoenix5 import TalonSRX,ControlMode
from wpilib import SmartDashboard

class Yaw:
    def __init__(self):
        self.position2 = None
        self.position1 = None
        self.p_position_units = None
        self.yaw_motor = TalonSRX(13)
        self.middle_position = 2393  # units
        self.step = 20  # units

    def init_motor(self):
        self.yaw_motor.set(ControlMode.Position, self.middle_position)

    def control(self, button1, button2):
        self.p_position_units = self.yaw_motor.getSelectedSensorPosition()
        # self.p_position_deg = self.p_position_units/4096*360
        if 1870 < self.p_position_units < 2900:
            if button1:
                self.position1 = self.yaw_motor.getSelectedSensorPosition()
                self.yaw_motor.set(ControlMode.Position, self.position1 + self.step)
                # SmartDashboard.putNumber("sb1",90-((self.position1+self.step-self.middle_position)/4096*360))
            if button2:
                self.position2 = self.yaw_motor.getSelectedSensorPosition()
                self.yaw_motor.set(ControlMode.Position, self.position2 - self.step)
                # SmartDashboard.putNumber("sb2",90+((self.position2-self.step-self.middle_position)/4096*360))
            SmartDashboard.putNumber("Yaw Angle(deg)",
                                     90 + ((self.p_position_units - self.middle_position) / 4096 * 360))
        else:
            self.yaw_motor.set(ControlMode.Position, self.middle_position)

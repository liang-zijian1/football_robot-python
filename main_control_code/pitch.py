from phoenix5 import TalonSRX,ControlMode
from wpilib import SmartDashboard

class Pitch:
    def __init__(self):
        self.pitch_p_position_deg = None
        self.pitch_position2 = None
        self.pitch_position1 = None
        self.pitch_p_position_units = None
        self.pitch_motor1 = TalonSRX(15)
        self.pitch_motor2 = TalonSRX(16)
        self.pitch_max_position = 421  # units,最低点
        self.pitch_min_position = 25
        self.pitch_step =  40 # units

    def motor_init(self):
        self.pitch_motor1.set(ControlMode.Position, 350)
        self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())

    def control(self, pitch_button1, pitch_button2):
        self.pitch_p_position_units = self.pitch_motor1.getSelectedSensorPosition()
        #print(self.pitch_p_position_units)
        # self.pitch_p_position_deg = self.pitch_p_position_units / 4096 * 360
        if self.pitch_min_position < self.pitch_p_position_units < self.pitch_max_position:
            if pitch_button1:
                self.pitch_position1 = self.pitch_motor1.getSelectedSensorPosition()
                self.pitch_motor1.set(ControlMode.Position, self.pitch_position1 - self.pitch_step)
                self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())
                # SmartDashboard.putNumber("sb1",90-((self.position1+self.step-self.middle_position)/4096*360))
            if pitch_button2:
                self.pitch_position2 = self.pitch_motor1.getSelectedSensorPosition()
                self.pitch_motor1.set(ControlMode.Position, self.pitch_position2 + self.pitch_step)
                self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())
                # SmartDashboard.putNumber("sb2",90+((self.position2-self.step-self.middle_position)/4096*360))
            SmartDashboard.putNumber("Pitch Angle(deg)", (self.pitch_p_position_units-25) / 4096 * 360)
        else:
            self.pitch_motor1.set(ControlMode.Position, 350)
            self.pitch_motor2.set(ControlMode.Follower, self.pitch_motor1.getDeviceID())
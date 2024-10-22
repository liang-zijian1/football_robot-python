from phoenix5 import VictorSPX,VictorSPXControlMode
class Ballpipe:
    def __init__(self):
        self.Ballpipe_motor = VictorSPX(2)
        
    def control(self,button):
        if button==True:
            self.Ballpipe_motor.set(VictorSPXControlMode.PercentOutput, -1)
        else:
            self.Ballpipe_motor.set(VictorSPXControlMode.PercentOutput, 0)
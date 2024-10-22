import wpilib
from phoenix6.hardware import TalonFX
from phoenix6.controls import PositionDutyCycle,DutyCycleOut

class Roll:
    def __init__(self):
        self.roll_motor = TalonFX(14)
        self.dio_input = wpilib.DigitalInput(9)
        self.init_position = None
        self.init_step = 0.505527
        self.is_initialized = False

    def init_motor(self):
        # 每次重新启用时手动调用
        self.is_initialized = False  # 每次重新启用时重置

    def periodic_motor_control(self,pov):
        # 在teleopPeriodic中持续调用
        dio_state = self.dio_input.get()
        if dio_state == False and not self.is_initialized:
            self.init_position = self.roll_motor.get_position().value_as_double
            self.roll_motor.set_control(PositionDutyCycle(self.init_position - self.init_step))
            self.is_initialized = True  # 标记已归中
        elif not self.is_initialized:
            # 如果尚未归中，继续转动电机直到检测到 False
            self.roll_motor.set_control(DutyCycleOut(0.046))
        else:
            # 电机已归中，可以进行其他操作
            if pov==90:
                self.roll_motor.set_control(PositionDutyCycle(self.init_position))
            if pov==270:
                self.roll_motor.set_control(PositionDutyCycle(self.init_position-self.init_step*2))
            if pov==0:
                self.roll_motor.set_control(PositionDutyCycle(self.init_position - self.init_step))
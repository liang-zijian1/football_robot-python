# TODO: insert robot code here
import magicbot
import wpilib
import phoenix6
import rev
import commands2
import navx
import xrp


class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.controller = wpilib.Joystick(0)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
   

    def teleopPeriodic(self):
          # 读取左摇杆的X和Y值
        left_x = self.controller.getX(wpilib.Joystick.Hand.kLeft)
        left_y = self.controller.getY(wpilib.Joystick.Hand.kLeft)
        
        # 读取右摇杆的X和Y值
        right_x = self.controller.getX(wpilib.Joystick.Hand.kRight)
        right_y = self.controller.getY(wpilib.Joystick.Hand.kRight)
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingImports=false
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, Motor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from htcolor import HTColor
from wroRobot import WroRobot
from time import sleep, time
import sys
import os
from ev3dev2.button import Button
from ev3dev2.led import Leds
import threading

os.system('setfont Lat15-TerminusBold32x16')

class Task:
    def __init__(self, robot: WroRobot):
        # password: "maker"
        
        self.robot = robot
        self.leds = Leds()
        self.button = Button()
        self.grabber = MediumMotor(address=OUTPUT_A)
        self.emelo = MediumMotor(address=OUTPUT_D)
        self.emelo.polarity = Motor.POLARITY_INVERSED
        # pozitív degrees -> Befele
        # pozitív degrees -> Felfele


    def e_g_nulla(self, var = True, speed = 100):
        if var == True:
            self.grabber.on_to_position(speed=speed, position=0, block=True)
            self.emelo.on_to_position(speed=speed, position=0, block=True)
        else:
            self.grabber.on_to_position(speed=speed, position=0, block=False)
            self.emelo.on_to_position(speed=speed, position=0, block=False)

    def vege(self):
        self.robot.gyroadatok.close()
        self.grabber.on_to_position(speed=100, position=0, block=False)
        self.emelo.on_to_position(speed=100, position=0, block=True)
        exit()

    def startup(self):
        self.robot.forwardCmWithGyro(speed=500, angle=0, distance=5)
        self.robot.forwardCm(speed=500, distance=-5)
        self.grabber.on_for_degrees(speed=100, degrees=400, block=False)
        self.emelo.on_for_degrees(speed=100, degrees=300, block=True)
        self.e_g_nulla()





    def rohadjmeg(self):
        self.grabber.stop_action = 'hold'
        self.emelo.stop_action = 'hold'
        self.grabber.position = 0
        self.emelo.position = 0

        # előre megy a 1. 3 kockához és megfogja
        self.robot.forwardCmWithGyro(speed=800, distance=12, angle=0)
        self.grabber.on_to_position(speed=40, position=100, block=True)
        # megfogja a kockákat a belsejébe
        self.robot.forwardCmWithGyro(speed=800, distance=-19, angle=0)
        self.grabber.on_to_position(speed=40, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
        self.grabber.on_to_position(speed=100, position=110)
        # self.grabber.on_to_position(speed=100, position=0)
        # self.grabber.on_to_position(speed=100, position=110)
        # elviszi a kockákat a helyére
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=43, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        # feketere egyenesedes 0 fokon
        self.robot.alignToBlack(speed=800, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=38, angle=0)
        # feketere egyenesedes 0 fokon
        self.robot.alignToBlack(speed=200)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
        # elfordul a mozaik felé
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.grabber.on_to_position(speed=100, position=300, block=True)
        self.emelo.on_to_position(speed=45, position=250)
        self.robot.forwardCmWithGyro(speed=800, distance=20, angle=90)
        self.robot.alignToBlack(speed=200)
        # 90 fokra fordul a mozaik előtt, majd beviszi a 1*3 kockát
        self.robot.turnToGyroAngle(speed=200, angle=90)
        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=500, distance=29, angle=90)
        self.grabber.stop()
        self.grabber.on_to_position(speed=100, position=0)
        # hárta megy a fekete vonalig
        self.robot.forwardCmWithGyro(speed=500, distance=-65, angle=90)
        self.robot.alignToBlack(speed=-200)
        self.e_g_nulla()

    def masodik(self):
        # elmegy a 2. 1*3 kockáért
        self.robot.turnToGyroAngle(speed=200, angle=180)
        self.robot.forwardCmWithGyro(speed=800, distance=32, angle=180)
        self.robot.alignToBlack(speed=200)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=180)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=-25.5, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        # felveszi az 1*3 kockát
        self.robot.forwardCmWithGyro(speed=800, distance=3, angle=0)
        self.grabber.on_to_position(speed=100, position=100)
        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=800, distance=-25, angle=0)
        self.grabber.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
        self.grabber.on_to_position(speed=100, position=110)
        # self.grabber.on_to_position(speed=100, position=0)
        # self.grabber.on_to_position(speed=100, position=110)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        # elviszi a kockákat
        self.robot.forwardCmWithGyro(speed=800, distance=41, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        self.robot.alignToBlack(speed=500, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=38, angle=0)
        # vonalra áll 0 fokon
        self.robot.alignToBlack(speed=200)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.grabber.on_to_position(speed=100, position=300, block=True)
        self.emelo.on_to_position(speed=45, position=500)
        self.robot.forwardCmWithGyro(speed=800, distance=20, angle=90)
        # vonalra áll 0 fokon
        self.robot.alignToBlack(speed=200)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        # self.robot.buttonPress()
        # beviszi a 2. 1*3 kockát
        self.robot.forwardCmWithGyro(speed=800, distance=22, angle=90)
        self.grabber.stop()
        self.emelo.on_to_position(speed=100, position=300)
        self.grabber.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=-60, angle=90)
        self.robot.alignToBlack(speed=-200)
        self.e_g_nulla()
        

    def harmadik(self):
        # elmegy a 3. 1*3 kockáért
        self.robot.turnToGyroAngle(speed=200, angle=180)
        self.robot.forwardCmWithGyro(speed=800, distance=20, angle=180)
        self.robot.alignToBlackWithSide(speed=400, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=180)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=-25.5, angle=90)
        self.robot.egyenesedes(speed=400, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=20, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        # felveszi az 1*3 kockát

        self.robot.forwardCmWithGyro(speed=800, distance=3, angle=0)
        self.grabber.on_to_position(speed=100, position=100)
        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=800, distance=-25, angle=0)
        self.grabber.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
        self.grabber.on_to_position(speed=100, position=110)
        # self.grabber.on_to_position(speed=100, position=0)
        # self.grabber.on_to_position(speed=100, position=110)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        # elviszi a kockákat
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=90)
        self.robot.alignToBlack(speed=500)
        self.robot.forwardCmWithGyro(speed=800, distance=15, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        self.robot.forwardCmWithGyro(speed=800, distance=38, angle=0)
        # vonalra áll 0 fokon
        self.robot.alignToBlack(speed=200)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=15, angle=90)
        self.grabber.stop()
        self.emelo.on_to_position(speed=100, position=300)
        self.grabber.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=-50, angle=90)
        self.robot.alignToBlack(speed=-200)
        self.e_g_nulla()

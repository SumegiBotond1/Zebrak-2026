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

    def felvesz(self):
        self.grabber.on_to_position(speed=100, position=150)
        self.grabber.on_to_position(speed=100, position=0)
        sleep(0.2)
        self.grabber.on_to_position(speed=100, position=150)


    def rohadjmeg(self):
        # előre megy a 1. 3 kockához és megfogja
        self.robot.forwardCmWithGyro(speed=800, distance=10.8, angle=0)
        self.grabber.on_to_position(speed=40, position=120, block=True)
        # megfogja a kockákat a belsejébe
        self.robot.forwardCmWithGyro(speed=800, distance=-19, angle=0)

        self.grabber.on_to_position(speed=40, position=0)

        self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
        self.felvesz()

        # elmegy felvelnni a 2. 3 kockát
        self.emelo.on_to_position(speed=80, position=400)

        self.robot.forwardCmWithGyro(speed=800, distance=14, angle=0)

        self.emelo.on_to_position(speed=80, position=0)

        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=800, distance=-14, angle=0)

        # elviszi a 1.,2. 3 kockát a helyére
        self.robot.turnToGyroAngle(speed=300, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=43, angle=90)
        self.robot.turnToGyroAngle(speed=300, angle=0)

        self.robot.forwardCmWithGyro(speed=800, distance=42, angle=0)
        # feketere egyenesedes
        self.robot.alignToBlack(speed=300, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
        # elfordul, hogy lerakja a 2. 3 kockát
        self.robot.turnToGyroAngle(speed=300, angle=-90)

        self.robot.forwardCmWithGyro(speed=800, distance=-7, angle=-90)
        self.emelo.on_to_position(speed=80, position=400)
        # self.robot.forwardCmWithGyro(speed=800, distance=-14, angle=-90)
        # beviszi a 1. 3 kockát
        self.robot.turnToGyroAngle(speed=300, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=6, angle=90)
        self.robot.alignToBlack(speed=200, blackThreshold=18.5)

        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=500, distance=25.8, angle=90)
        self.emelo.on_to_position(speed=100, position=60)
        self.grabber.stop()
        self.grabber.on_to_position(speed=40, position=0)

        # hárta megy a felvelnni a 2. 3 kockát
        self.robot.forwardCmWithGyro(speed=500, distance=-7, angle=90)
        self.emelo.on_to_position(speed=80, position=0, block=False)
        self.robot.forwardCmWithGyro(speed=500, distance=-25, angle=90)
        self.robot.alignToBlack(speed=200, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=500, distance=-10, angle=90)
        self.robot.turnToGyroAngle(speed=300, angle=-90)
        self.robot.forwardCmWithGyro(speed=800, distance=15, angle=-87.8)
        self.robot.alignToBlack(speed=200, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=2, angle=-90)
        # self.robot.buttonPress()
        # felveszi a 2. 3 kockát
        self.felvesz()
        self.robot.turnToGyroAngle(speed=300, angle=90)
        # beviszi a 2. 3 kockát
        self.robot.forwardCmWithGyro(speed=800, distance=24, angle=90)
        self.robot.alignToBlack(speed=200, blackThreshold=18.5)
        self.emelo.on_to_position(speed=80, position=500)

        self.robot.forwardCmWithGyro(speed=800, distance=22, angle=90)
        self.grabber.stop()
        self.emelo.on_to_position(speed=100, position=400)
        self.grabber.on_to_position(speed=100, position=0)

        # hátra megy a fekete vonalig
        self.robot.forwardCmWithGyro(speed=800, distance=-60, angle=90)
        self.robot.alignToBlack(speed=-200, blackThreshold=7)
        self.e_g_nulla()



    def masodik(self):
        # elmegy a 3.,4. 1*3 kockáért
        self.robot.turnToGyroAngle(speed=200, angle=180)
        self.robot.forwardCmWithGyro(speed=800, distance=28, angle=180)
        self.robot.alignToBlack(speed=200, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=180)
        self.robot.turnToGyroAngle(speed=200, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=-28, angle=90)
        # egyenesedik a falakhoz
        self.robot.egyenesedes(speed=-300, seconds=1.5)
        self.robot.forwardCmWithGyro(speed=800, distance=12, angle=90)
        self.robot.turnToGyroAngle(speed=200, angle=0)
        self.robot.forwardCmWithGyro(speed=800, distance=-6, angle=0)
        self.robot.egyenesedes(speed=-300, seconds=1.5)
        self.robot.writeGyroAngle()

        # elmegy felvelnni a 3.,4. 1*3 kockát
        # self.log("1")
        self.robot.forwardCmWithGyro(speed=800, distance=33.5, angle=0)
        self.grabber.on_to_position(speed=100, position=100)
        # self.log("2")
        # self.robot.buttonPress()
        self.robot.forwardCmWithGyro(speed=800, distance=-19, angle=0)
        self.grabber.on_to_position(speed=100, position=0)
        # felveszi a 3.,4. 1*3 kockát
        self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
        self.felvesz()

        self.emelo.on_to_position(speed=80, position=400)
        # self.robot.writeGyroAngle()
        self.robot.forwardCmWithGyro(speed=800, distance=17, angle=0)

        # self.robot.writeGyroAngle()
        self.emelo.on_to_position(speed=80, position=-10)
        self.robot.forwardCmWithGyro(speed=800, distance=-17, angle=0)


        # elviszi a 3.,4. 1*3 kocká
        self.robot.turnToGyroAngle(speed=300, angle=90)

        self.robot.forwardCmWithGyro(speed=800, distance=34.5, angle=90)
        self.robot.turnToGyroAngle(speed=300, angle=0)


        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=0)

        # egyenesedik a vonalhoz
        self.robot.alignToBlackWithSide(speed=400, blackThreshold=7, side="right")
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)

        # lerakja a 4. 1*3 kockát
        self.robot.turnToGyroAngle(speed=300, angle=-90)
        self.robot.forwardCmWithGyro(speed=800, distance=-11, angle=-90)
        self.robot.buttonPress()
        self.emelo.on_to_position(speed=80, position=500)

        self.robot.turnToGyroAngle(speed=300, angle=90)

        # beviszi a 3. 1*3 kockát
        self.robot.forwardCmWithGyro(speed=600, distance=13, angle=90)
        self.robot.alignToBlack(speed=200, blackThreshold=18.5)
        self.robot.forwardCmWithGyro(speed=500, distance=18.5, angle=90)
        self.emelo.on_to_position(speed=80, position=400)
        self.grabber.on_to_position(speed=40, position=0)
        self.robot.forwardCmWithGyro(speed=500, distance=-17, angle=90)
        self.robot.turnToGyroAngle(speed=300, angle=-90)
        self.emelo.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=600, distance=36, angle=-90.5)
        self.robot.buttonPress()
        # self.robot.alignToBlack(speed=200, blackThreshold=10)
        self.felvesz()
        # self.robot.buttonPress()
        # self.robot.alignToBlack(speed=-200, blackThreshold=7)

        self.robot.forwardCmWithGyro(speed=600, distance=-4, angle=-90.5)
        self.emelo.on_to_position(speed=80, position=500)
        self.robot.turnToGyroAngle(speed=300, angle=90)
        self.robot.forwardCmWithGyro(speed=600, distance=34, angle=89.5)
        self.robot.alignToBlack(speed=200, blackThreshold=18.5)
        self.robot.forwardCmWithGyro(speed=600, distance=13.5, angle=89.5)
        self.emelo.on_to_position(speed=100, position=400)
        self.grabber.on_to_position(speed=100, position=0)
        self.e_g_nulla()

















    # def rohadjmeg(self):
    #     self.grabber.stop_action = 'hold'
    #     self.emelo.stop_action = 'hold'
    #     self.grabber.position = 0
    #     self.emelo.position = 0

    #     # előre megy a 1. 3 kockához és megfogja
    #     self.robot.forwardCmWithGyro(speed=800, distance=12, angle=0)
    #     self.grabber.on_to_position(speed=40, position=100, block=True)
    #     # megfogja a kockákat a belsejébe
    #     self.robot.forwardCmWithGyro(speed=800, distance=-19, angle=0)
    #     self.grabber.on_to_position(speed=40, position=0)
    #     self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     # elviszi a kockákat a helyére
    #     self.robot.turnToGyroAngle(speed=300, angle=90)
    #     self.robot.forwardCmWithGyro(speed=800, distance=43, angle=90)
    #     self.robot.turnToGyroAngle(speed=300, angle=0)
    #     # feketere egyenesedes 0 fokon
    #     self.robot.alignToBlack(speed=400, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=38, angle=0)
    #     # feketere egyenesedes 0 fokon
    #     self.robot.alignToBlack(speed=300, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
    #     # elfordul a mozaik felé
    #     self.robot.turnToGyroAngle(speed=300, angle=90)
    #     self.grabber.on_to_position(speed=100, position=300, block=True)
    #     self.emelo.on_to_position(speed=100, position=250)
    #     self.robot.forwardCmWithGyro(speed=800, distance=20, angle=90)
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     # 90 fokra fordul a mozaik előtt, majd beviszi a 1*3 kockát
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     # self.robot.buttonPress()
    #     self.robot.forwardCmWithGyro(speed=500, distance=29, angle=90)
    #     self.grabber.stop()
    #     self.grabber.on_to_position(speed=100, position=0)
    #     # hárta megy a fekete vonalig
    #     self.robot.forwardCmWithGyro(speed=500, distance=-65, angle=90)
    #     self.robot.alignToBlack(speed=-200, blackThreshold=7)
    #     self.e_g_nulla()


    # def masodik(self):
    #     # elmegy a 2. 1*3 kockáért
    #     self.robot.turnToGyroAngle(speed=200, angle=180)
    #     self.robot.forwardCmWithGyro(speed=800, distance=32, angle=180)
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=4, angle=180)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     self.robot.forwardCmWithGyro(speed=800, distance=-26.5, angle=90)
    #     self.robot.egyenesedes(speed=-300, angle=90, seconds=1.5)
    #     self.robot.forwardCmWithGyro(speed=800, distance=12, angle=90)
    #     self.robot.turnToGyroAngle(speed=200, angle=0)
    #     # felveszi az 1*3 kockát
    #     self.robot.forwardCmWithGyro(speed=800, distance=3.5, angle=0)
    #     # self.robot.buttonPress()
    #     self.grabber.on_to_position(speed=100, position=100)
    #     # self.robot.buttonPress()
    #     self.robot.forwardCmWithGyro(speed=800, distance=-25, angle=0)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     # elviszi a kockákat
    #     self.robot.forwardCmWithGyro(speed=800, distance=41, angle=90)
    #     self.robot.turnToGyroAngle(speed=200, angle=0)
    #     self.robot.alignToBlack(speed=500, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=38, angle=0)
    #     # vonalra áll 0 fokon
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     self.grabber.on_to_position(speed=100, position=300, block=True)
    #     self.emelo.on_to_position(speed=45, position=500)
    #     self.robot.forwardCmWithGyro(speed=800, distance=20, angle=90)
    #     # vonalra áll 0 fokon
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     # self.robot.buttonPress()
    #     # beviszi a 2. 1*3 kockát
    #     self.robot.forwardCmWithGyro(speed=800, distance=22, angle=90)
    #     self.grabber.stop()
    #     self.emelo.on_to_position(speed=100, position=300)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.robot.forwardCmWithGyro(speed=800, distance=-60, angle=90)
    #     self.robot.alignToBlack(speed=-200, blackThreshold=7)
    #     self.e_g_nulla()


    # def harmadik(self):
    #     # elmegy a 3. 1*3 kockáért
    #     self.robot.turnToGyroAngle(speed=200, angle=180)
    #     self.robot.forwardCmWithGyro(speed=800, distance=10, angle=180)
    #     self.robot.alignToBlackWithSide(speed=400, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=10, angle=180)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     self.robot.forwardCmWithGyro(speed=800, distance=-25.5, angle=90)
    #     self.robot.egyenesedes(speed=-300, angle=90, seconds=1.5)
    #     self.robot.forwardCmWithGyro(speed=800, distance=12, angle=90)
    #     self.robot.turnToGyroAngle(speed=200, angle=0)
    #     # felveszi az 1*3 kockát

    #     self.robot.forwardCmWithGyro(speed=800, distance=3, angle=0)
    #     self.grabber.on_to_position(speed=100, position=100)
    #     # self.robot.buttonPress()
    #     self.robot.forwardCmWithGyro(speed=800, distance=-15, angle=0)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.robot.forwardCmWithGyro(speed=800, distance=9, angle=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.grabber.on_to_position(speed=100, position=110)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     # elviszi a kockákat
    #     self.robot.forwardCmWithGyro(speed=800, distance=37, angle=90)
    #     self.robot.turnToGyroAngle(speed=200, angle=1)
    #     self.robot.forwardCmWithGyro(speed=800, distance=20, angle=0)
    #     # vonalra áll 0 fokon
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     self.robot.forwardCmWithGyro(speed=800, distance=18, angle=90)
    #     self.emelo.on_to_position(speed=45, position=500)
    #     self.robot.alignToBlack(speed=200, blackThreshold=7)
    #     self.robot.turnToGyroAngle(speed=200, angle=90)
    #     self.grabber.on_to_position(speed=100, position=300, block=True)
    #     self.robot.forwardCmWithGyro(speed=800, distance=17, angle=90)
    #     self.grabber.stop()
    #     self.emelo.on_to_position(speed=100, position=300)
    #     self.grabber.on_to_position(speed=100, position=0)
    #     self.robot.forwardCmWithGyro(speed=800, distance=-50, angle=90)
    #     self.robot.alignToBlack(speed=-200, blackThreshold=7)
    #     self.e_g_nulla()

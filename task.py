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
        self.robot = robot
        self.leds = Leds()
        self.button = Button()
        self.grabber = MediumMotor(address=OUTPUT_A)
        self.emelo = MediumMotor(address=OUTPUT_D)
        self.emelo.polarity = Motor.POLARITY_INVERSED

    def e_g_nulla(self, speed = 100, block=True):
        if block:
            self.grabber.on_to_position(speed=speed, position=0, block=True)
            self.emelo.on_to_position(speed=speed, position=0, block=True)
        else:
            self.grabber.on_to_position(speed=speed, position=0, block=False)
            self.emelo.on_to_position(speed=speed, position=0, block=False)



    def startup(self):
        self.robot.forwardCmWithGyro(speed=500, angle=0, distance=5)
        self.robot.forwardCm(speed=500, distance=-5)
        self.grabber.on_for_degrees(speed=100, degrees=400, block=False)
        self.emelo.on_for_degrees(speed=100, degrees=300, block=True)
        self.e_g_nulla(speed=100, block=False)

    def felvesz(self, speed=100):
        self.grabber.on_to_position(speed=speed, position=150, block=True)
        self.grabber.on_to_position(speed=speed, position=0, block=True)
        sleep(0.1)
        self.grabber.on_to_position(speed=speed, position=150, block=True)


    def rohadjmeg(self):

        self.robot.forwardCmWithGyro(speed=800, distance=10.8, angle=0)
        self.grabber.on_to_position(speed=40, position=120, block=True)


        self.robot.forwardCmWithGyro(speed=800, distance=-19, angle=0)

        self.grabber.on_to_position(speed=40, position=0)

        self.robot.forwardCmWithGyro(speed=800, distance=23, angle=0)
        self.felvesz(speed=50)



        self.robot.turnToGyroAngle(speed=400, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=38, angle=90)
        self.robot.turnToGyroAngle(speed=400, angle=0)

        self.robot.forwardCmWithGyro(speed=800, distance=23, angle=0)

        self.robot.alignToBlackWithSide(speed=400, right_threshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=2, angle=0)


        self.robot.turnToGyroAngle(speed=400, angle=-92)
        self.robot.forwardCmWithGyro(speed=800, distance=-13, angle=-90)
        self.emelo.on_to_position(speed=80, position=400)



        self.robot.turnToGyroAngle(speed=400, angle=90)
        self.emelo.on_to_position(speed=100, position=140, block=False)
        self.robot.forwardCmWithGyro(speed=800, distance=6, angle=91)
        self.robot.alignToBlack(speed=400, blackThreshold=18.5)


        self.robot.forwardCmWithGyro(speed=500, distance=28, angle=90)

        self.grabber.on_to_position(speed=40, position=0)



        self.robot.forwardCmWithGyro(speed=500, distance=-40, angle=90)
        self.emelo.on_to_position(speed=80, position=0, block=False)
        self.robot.turnToGyroAngle(speed=400, angle=-90)
        self.robot.forwardCmWithGyro(speed=800, distance=15, angle=-90)
        self.robot.alignToBlack(speed=550, blackThreshold=7)
        self.robot.forwardCmWithGyro(speed=900, distance=3, angle=-90)



        self.felvesz(speed=100)
        self.robot.turnToGyroAngle(speed=400, angle=90)


        self.emelo.on_to_position(speed=80, position=340, block=False)
        self.robot.forwardCmWithGyro(speed=800, distance=26, angle=89)
        self.robot.alignToBlack(speed=400, blackThreshold=18.5)

        self.robot.forwardCmWithGyro(speed=800, distance=23.7, angle=90)

        self.grabber.on_to_position(speed=100, position=0)


        self.robot.forwardCmWithGyro(speed=800, distance=-45, angle=90)
        self.robot.alignToBlack(speed=-400, blackThreshold=7)
        self.e_g_nulla(speed=100, block=False)



    def masodik(self):

        self.robot.turnToGyroAngle(speed=400, angle=180)
        self.robot.forwardCmWithGyro(speed=800, distance=28, angle=180)
        self.robot.alignToBlackWithSide(speed=400, left_threshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=180)
        self.robot.turnToGyroAngle(speed=400, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=-30, angle=90)


        self.robot.egyenesedes(speed=-300, seconds=1.5)
        self.robot.forwardCmWithGyro(speed=800, distance=11, angle=90)
        self.robot.turnToGyroAngle(speed=400, angle=2)
        self.robot.egyenesedes(speed=-300, seconds=2)



        self.robot.forwardCmWithGyro(speed=800, distance=33.5, angle=-2)
        self.grabber.on_to_position(speed=100, position=100)
        self.robot.forwardCmWithGyro(speed=800, distance=-25, angle=-2)
        self.grabber.on_to_position(speed=100, position=0)



        self.robot.forwardCmWithGyro(speed=800, distance=21, angle=-2)
        self.felvesz()



        self.robot.turnToGyroAngle(speed=400, angle=90)

        self.robot.forwardCmWithGyro(speed=800, distance=34.5, angle=90)
        self.robot.turnToGyroAngle(speed=400, angle=0)


        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=0)


        self.robot.alignToBlackWithSide(speed=400, right_threshold=7)
        self.robot.forwardCmWithGyro(speed=800, distance=4, angle=0)


        self.robot.turnToGyroAngle(speed=400, angle=-92)
        self.robot.forwardCmWithGyro(speed=800, distance=-11, angle=-90)
        self.emelo.on_to_position(speed=80, position=340)

        self.robot.turnToGyroAngle(speed=400, angle=90)


        self.robot.forwardCmWithGyro(speed=600, distance=13, angle=90)
        self.robot.alignToBlack(speed=400, blackThreshold=18.5)
        self.robot.forwardCmWithGyro(speed=500, distance=17, angle=90)
        self.grabber.on_to_position(speed=40, position=0)
        self.robot.forwardCmWithGyro(speed=500, distance=-20, angle=90)
        self.robot.turnToGyroAngle(speed=400, angle=-90)
        self.emelo.on_to_position(speed=100, position=0, block=False)
        self.robot.forwardCmWithGyro(speed=600, distance=16, angle=-88.5)
        self.robot.alignToBlack(speed=400, blackThreshold=13)
        self.robot.forwardCmWithGyro(speed=1200, distance=5, angle=-87.8)
        self.felvesz()


        self.emelo.on_to_position(speed=80, position=340, block=False)
        self.robot.forwardCmWithGyro(speed=600, distance=-4, angle=-88.5)
        self.robot.turnToGyroAngle(speed=400, angle=90)
        self.robot.forwardCmWithGyro(speed=600, distance=34, angle=87)
        self.robot.alignToBlack(speed=400, blackThreshold=18.5)
        self.robot.forwardCmWithGyro(speed=600, distance=11.5, angle=90)
        self.grabber.on_to_position(speed=100, position=0)
        self.robot.forwardCmWithGyro(speed=800, distance=-45, angle=90)
        self.robot.alignToBlack(speed=-400, blackThreshold=7)
        self.e_g_nulla(speed=100, block=False)


    def ni(self):
        self.robot.turnToGyroAngle(speed=400, angle=0)
        self.robot.forwardCmWithGyro(speed=800, distance=-50, angle=0)
        self.robot.egyenesedes(speed=-400, angle=0, seconds=1.5)

        self.grabber.on_to_position(speed=100, position=0, block=False)
        self.robot.turnToGyroAngle(angle=90, left_speed=700)
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=90)
        self.robot.alignToBlackWithSide(speed=500, right_threshold=30)
        self.robot.forwardCmWithGyro(speed=800, distance=4.2, angle=90)
        self.grabber.on_to_position(speed=100, position=70, block=True)
        self.robot.forwardCmWithGyro(speed=800, distance=-30, angle=90)
        self.grabber.on_to_position(speed=70, position=0, block=True)

        self.robot.forwardCmWithGyro(speed=800, distance=-10, angle=90)
        self.robot.turnToGyroAngle(speed=400, angle=45)
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=45)
        self.robot.turnToGyroAngle(speed=400, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=45, angle=90)
        self.grabber.on_to_position(speed=100, position=-20, block=False)
        self.robot.turnToGyroAngle(angle=135, left_speed=700)
        #PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  | | | |
        #ÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ \/\/\/\/
        # self.robot.forwardCmWithGyro(speed=800, distance=3.14159265358979323846, angle=135)
        self.robot.forwardCmWithGyro(speed=800, distance=2.5, angle=135)
        self.robot.turnToGyroAngle(angle=90, right_speed=700)
        self.robot.forwardCmWithGyro(speed=800, distance=10, angle=90)
        self.grabber.on_to_position(speed=100, position=70, block=True)
        self.robot.turnToGyroAngle(right_speed=700, angle=45)
        self.robot.alignToBlackWithSide(speed=400, left_threshold=10)
        self.robot.turnToGyroAngle(speed=700, angle=90)
        self.robot.forwardCmWithGyro(speed=800, distance=40, angle=90)
        self.robot.turnToGyroAngle(angle=0, right_speed=700)
        self.robot.forwardCmWithGyro(speed=800, distance=12, angle=0)
        self.e_g_nulla()
        self.robot.forwardCmWithGyro(speed=1500, distance=-7, angle=0)

        self.robot.turnToGyroAngle(speed=500, angle=360)
        self.robot.forwardCmWithGyro(speed=800, distance=5, angle=360)
        self.grabber.on_to_position(speed=100, position=120)
        self.robot.turnToGyroAngle(angle=270, left_speed=700)
        self.robot.forwardCmWithGyro(speed=100, distance=140, angle=271)
        self.e_g_nulla(block=True)





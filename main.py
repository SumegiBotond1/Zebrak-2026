#!/usr/bin/env python3
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingImports=false

from ev3dev2.motor import MediumMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D,  SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.power import PowerSupply
from ev3dev2.console import Console
from wroRobot import WroRobot
from task import Task
from time import time, sleep
import ev3dev2.fonts as fonts
import sys

button = Button()
leds = Leds()
sound = Sound()

def error(e):
    # sound.speak("ERROR")
    leds.set_color('LEFT', 'RED')
    leds.set_color('RIGHT', 'RED')
    while not button.enter:
        pass

    f = open('error.txt', 'w')
    print("Error: \n\t{}\n\n\n\n".format(e), file=sys.stderr)
    f.write("Error: \n\t{}".format(e))
    Not_working = []
    Motor_ports = [OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D]
    for port in Motor_ports:
        try:
            motor = MediumMotor(port)
            motor.on_for_seconds(speed=50, seconds=0.5)
            motor.on_to_position(speed=100, position=0)
        except:
            Not_working.append(port)
    Sensor_ports = [INPUT_1, INPUT_2, INPUT_3, INPUT_4]
    for port in Sensor_ports:
        try:
            if port == INPUT_1:
                s = GyroSensor(port)
                print("Test angle: {}".format(s.angle), file=sys.stderr)
                f.write("Test angle: {}\n".format(s.angle))
            else:
                s = ColorSensor(port)
                print("Test reflected: {}".format(s.reflected_light_intensity), file=sys.stderr)
                f.write("Test reflected: {}\n".format(s.reflected_light_intensity))
        except:
            Not_working.append(port)
    print("Ports that are not connected: {}".format(Not_working), file=sys.stderr)
    f.write("Ports that are not connected: {}\n".format(Not_working))
    f.close()


try:
    robot = WroRobot()
    # robot.calibrate()
    task = Task(robot)
    try:

        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'AMBER')
        robot.starting()
        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'AMBER')
        task.grabber.stop_action = 'hold'
        task.emelo.stop_action = 'hold'
        task.grabber.position = 0
        task.emelo.position = 0
        robot.writeGyroAngle()
        start_time = time()
        task.rohadjmeg()
        task.masodik()
        task.ni()
        robot.log("Time: {:.4f}s".format((time() - start_time)))
    except Exception as f:
        robot.log(f)
    finally:
        robot.stop()
        robot.gyroadatok.close()
        exit()
except Exception as e:
    print("Error: {}".format(e), file=sys.stderr)
    error(e)
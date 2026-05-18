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
    leds.set_color('LEFT', 'RED')
    leds.set_color('RIGHT', 'YELLOW')
    while not button.enter:
        pass
    print(f"Error: \n\t{e}\n", file=sys.stderr)
    not_working = []
    
    with open('error.txt', 'w') as f:
        f.write(f"Error: \n\t{e}")
        for port in [OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D]:
            try:
                motor = MediumMotor(port)
                motor.on_for_seconds(speed=50, seconds=0.5)
                motor.on_to_position(speed=100, position=0)
            except Exception:
                not_working.append(port)
        for port in [INPUT_1, INPUT_2, INPUT_3]:
            try:
                s = GyroSensor(port) if port == INPUT_1 else ColorSensor(port)
                val_type, val = ("angle", s.angle) if port == INPUT_1 else ("reflected", s.reflected_light_intensity)
                
                msg = f"Test {val_type}: {val}\n"
                print(msg, file=sys.stderr, end="")
                f.write(msg)
            except Exception:
                not_working.append(port)
        summary = f"Ports that are not connected: {not_working}\n"
        print(summary, file=sys.stderr, end="")
        f.write(summary)





try:
    robot = WroRobot()
    # robot.calibrate()
    task = Task(robot)
    try:
        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'GREEN')
        robot.starting()
        leds.set_color('LEFT', 'AMBER')
        leds.set_color('RIGHT', 'GREEN')
        task.grabber.stop_action = 'hold'
        task.emelo.stop_action = 'hold'
        task.grabber.position = 0
        task.emelo.position = 0
        robot.start_time = time()
        task.rohadjmeg()
        task.masodik()
        task.ni()
        task.final_time()
        robot.gyroadatok.close()
        robot.stop()
    except Exception as f:
        robot.log(f)
except Exception as e:
    print("Error: {}".format(e), file=sys.stderr)
    error(e)
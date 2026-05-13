from ev3dev2.motor import MediumMotor, Motor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.power import PowerSupply
from ev3dev2.stopwatch import StopWatch
import ev3dev2.fonts as fonts
from myColorSensor import MyColorSensor
import sys, time, os, threading
import ev3fast
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingImports=false
    
class WroRobot:

    def __init__(self, leftMotorPort = OUTPUT_B, rightMotorPort = OUTPUT_C, rightColorSensorPort = INPUT_2, leftColorSensorPort = INPUT_3, gyroSensorPort = INPUT_1):
        self.leds = Leds()
        self.gyroCorrection = 0

        self.left_motor = Motor(leftMotorPort)
        self.right_motor = Motor(rightMotorPort)
        self.left_motor.polarity = Motor.POLARITY_INVERSED

        self.left_motor.ramp_up_sp = 500
        self.right_motor.ramp_up_sp = 500

        if (leftColorSensorPort != None):
            self.leftColorSensor = MyColorSensor(port = leftColorSensorPort)
        else:
            self.leftColorSensor = None

        if (rightColorSensorPort != None):
            self.rightColorSensor = MyColorSensor(port = rightColorSensorPort)
        else:
            self.rightColorSensor = None

        if (gyroSensorPort != None):
            gyro = GyroSensor(gyroSensorPort)
            gyro.calibrate()
            gyro.reset()

            self.gyroSensor = ev3fast.GyroSensor(address = gyroSensorPort)
            # self.gyroSensor.calibrate()
            # self.gyroSensor.reset()
        else:
            self.gyroSensor = None

        self.gyroadatok = open("gyroadat.txt", "w")
        self.stopWatch = StopWatch()
        self.stopWatch.start()
        self.sound = Sound()
        self.display = Display()
        self.startLog()

    def calibrate(self):
        self.leds.set_color('LEFT', 'AMBER')
        self.leds.set_color('RIGHT', 'AMBER')
        self.leftColorSensor.calibrate()
        self.rightColorSensor.calibrate()
        self.leds.set_color('LEFT', 'GREEN')
        self.leds.set_color('RIGHT', 'GREEN')
        # self.checkColorAlign()

    def starting(self):
        self.display.draw.text((10,10), 'I`m ready!', font=fonts.load('luBS24'))
        self.display.update()
        # self.sound.tone([(500, 150, 50), (500, 150, 50)])

        powerSupply = PowerSupply()
        button = Button()

        count = 0
        self.log("Gyrocorrection: {}".format(self.gyroCorrection))
        while not button.enter:
            if powerSupply.measured_volts < 7.8 and count < 1:
                self.sound.speak("Lawu voultaege")
                count += 1
            pass

        self.stopWatch.stop()
        self.stopWatch.reset()
        self.stopWatch.start()

    def forwardSeconds(self, speed, seconds):
        self.left_motor.run_timed(speed_sp=speed, time_sp=seconds*1000)
        self.right_motor.run_timed(speed_sp=speed, time_sp=seconds*1000)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()
        
    def stop(self):
        self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()
        
    def alignToBlack(self, speed, blackThreshold = None):
        self.left_motor.run_forever(speed_sp = speed)
        self.right_motor.run_forever(speed_sp = speed)
        while (self.left_motor.is_running or self.right_motor.is_running):
            if (self.leftColorSensor.isBlackReflection(blackThreshold)): 
                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            if (self.rightColorSensor.isBlackReflection(blackThreshold)):
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.stop()

    def alignToMaxBlue(self, speed, blueMaxTreshold = 30):
        try:
            self.leftColorSensor.mode = ColorSensor.MODE_RGB_RAW
            self.rightColorSensor.mode = ColorSensor.MODE_RGB_RAW
            
            time.sleep(0.5)
            self.left_motor.run_forever(speed_sp = speed)            
            self.right_motor.run_forever(speed_sp = speed)            
            while (self.left_motor.is_running or self.right_motor.is_running):
                if (self.leftColorSensor.rgb[2] < blueMaxTreshold or (self.rightColorSensor.rgb[2] < blueMaxTreshold)):
                    self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            self.stop()
        except:
            pass
        self.leftColorSensor.mode = ColorSensor.MODE_REF_RAW
        self.rightColorSensor.mode = ColorSensor.MODE_REF_RAW

    def forwardCmWithGyro(self, speed, distance, angle, stop = True):
        angle = angle * 1
        degrees = distance * (360 / 17.6)
        self.forwardAngleWithGyro(speed, degrees, angle, stop)

    def forwardAngleWithGyro(self, speed, degrees, angle, stop = True):
        self.left_motor.position = 0        
        self.right_motor.position = 0        
        if speed * degrees > 0:
            wf = lambda robot : robot.left_motor.position < abs(degrees)
            self.forwardWithGyro(abs(speed), angle, wf, stop)
        else:
            wf = lambda robot : robot.left_motor.position > -abs(degrees)
            self.forwardWithGyro(-abs(speed), angle, wf, stop)

    def forwardWithGyro(self, speed, angle, while_func, stop = True):
        sign = speed / abs(speed)

        left_speed = 50 * sign
        right_speed = 50 * sign
        while while_func(self):
            self.left_motor.run_forever(speed_sp = int(left_speed))
            self.right_motor.run_forever(speed_sp = int(right_speed))
            
            if speed > 0:
                if right_speed < speed or left_speed < speed:
                    left_speed += 15
                    right_speed += 15
                
                diff_speed = (angle - (self.gyroSensor.angle - self.gyroCorrection)) * 10

                if diff_speed < 0:
                    if right_speed >= speed:
                        right_speed = speed
                        left_speed = speed - abs(diff_speed)
                    else:
                        right_speed = left_speed + abs(diff_speed)
                elif diff_speed > 0:
                    if left_speed >= speed:
                        left_speed = speed
                        right_speed = speed - abs(diff_speed)
                    else:
                        left_speed = right_speed + abs(diff_speed)
                elif left_speed != right_speed:
                    if left_speed > speed or right_speed > speed:
                        left_speed = speed
                        right_speed = speed
                    else:
                        left_speed = max(left_speed, right_speed)
                        right_speed = left_speed
            else:
                if right_speed > speed or left_speed > speed:
                    left_speed -= 15
                    right_speed -= 15
                
                diff_speed = (angle - (self.gyroSensor.angle- self.gyroCorrection)) * 10
                

                if diff_speed > 0:
                    if right_speed <= speed:
                        right_speed = speed
                        left_speed = speed + abs(diff_speed)
                    else:
                        right_speed = left_speed - abs(diff_speed)
                elif diff_speed < 0:
                    if left_speed <= speed:
                        left_speed = speed
                        right_speed = speed + abs(diff_speed)
                    else:
                        left_speed = right_speed - abs(diff_speed)
                elif left_speed != right_speed:
                    if left_speed < speed or right_speed < speed:
                        left_speed = speed
                        right_speed = speed
                    else:
                        left_speed = min(left_speed, right_speed)
                        right_speed = left_speed
        if stop:
            self.stop()

    def TurnXAngle(self, speed, angle):
        current = self.gyroSensor.angle - self.gyroCorrection
        target = current + angle
        self.turnToGyroAngle(angle=target, speed=speed)

    def turnToGyroAngle(self, angle, speed=200):
        current = self.gyroSensor.angle - self.gyroCorrection
        
        if current < angle:
            self.right_motor.run_forever(speed_sp=-abs(speed))
            self.left_motor.run_forever(speed_sp= abs(speed))
            while self.gyroSensor.angle - self.gyroCorrection < (angle - 2):
                pass
        else:
            self.right_motor.run_forever(speed_sp=abs(speed))
            self.left_motor.run_forever(speed_sp=-abs(speed))
            while self.gyroSensor.angle - self.gyroCorrection > (angle + 2):
                pass
        self.stop()
        
    def egyenesedes(self, angle=None, speed = 300, seconds=1.0):
        self.left_motor.run_timed(speed_sp=speed, time_sp=seconds*1000)
        self.right_motor.run_timed(speed_sp=speed, time_sp=seconds*1000)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()
        # if angle != None:
            # print("HIHI", file=sys.stderr)
            # time.sleep(0.01)
            # self.setGyroCorrection(angle)

    def alignToBlackWithSide(self, speed, blackThreshold = None, side="right"):
        self.left_motor.run_forever(speed_sp = speed)            
        self.right_motor.run_forever(speed_sp = speed)            
        while (self.left_motor.is_running or self.right_motor.is_running):
            if side == "right":
                if (self.rightColorSensor.isBlackReflection(blackThreshold)):
                    self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            elif side == "left":
                if (self.leftColorSensor.isBlackReflection(blackThreshold)):
                    self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.stop()

    def setGyroCorrection(self, angle):
        CurrentAngle = self.gyroSensor.angle
        self.gyroCorrection = CurrentAngle - angle







    def beep(self):
        self.sound.tone([(500, 150, 50)])
    
    def buttonPress(self):
        button = Button()
        while not button.enter:
            self.leds.set_color('LEFT', 'AMBER')
            self.leds.set_color('RIGHT', 'AMBER')
        self.leds.set_color('LEFT', 'GREEN')
        self.leds.set_color('RIGHT', 'GREEN')

    def kerek_tisztitas(self):
        button = Button()
        while not button.enter:
            pass
        self.left_motor.run_forever(speed_sp=700)
        self.right_motor.run_forever(speed_sp=700)
        self.leds.set_color('LEFT', 'YELLOW')
        self.leds.set_color('RIGHT', 'YELLOW')
        while not button.enter: 
            pass
        self.stop()

    def writeGyroAngle(self, nev = None):
        if nev == None:
            nev = "Angle"
        self.log("Angle: {}\n\tGyrocorrection: {}".format((self.gyroSensor.angle-self.gyroCorrection), self.gyroCorrection))
        self.gyroadatok.write("{}: {}\n".format(nev, self.gyroSensor.angle))
        self.gyroadatok.flush()

    def alignToWhite(self, speed, whiteThreshold = None):
        self.left_motor.run_forever(speed_sp = speed)            
        self.right_motor.run_forever(speed_sp = speed)            
        while (self.left_motor.is_running or self.right_motor.is_running):
            if (self.leftColorSensor.isWhiteReflection(whiteThreshold)):
                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            if (self.rightColorSensor.isWhiteReflection(whiteThreshold)):
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.stop()





    def startLog(self):
        try:
            os.mkdir("./log")
        except:
            pass

        logFiles = os.listdir("./log")
        i = 1
        if len(logFiles) > 0:
            logFiles.sort()
            i = int(logFiles[-1][4:7]) + 1

        self.logFileName = "./log/log_{0:03d}.txt".format(i)
        self.displayedEvents = []
        with open(self.logFileName, "w+") as f:
            pass
        print("Log file created: {0}".format(self.logFileName), file=sys.stderr)        

    def log(self, text, logtext=""):
        with open(self.logFileName, "a") as f:
            if logtext == "":
                f.write("{0:04.2f} - {1}\n".format(self.stopWatch.value_secs, text))
                print("Log ({0}): {1}".format(self.stopWatch.value_secs, text), file=sys.stderr)
            else:
                f.write("{0:04.2f} - {1}\n".format(self.stopWatch.value_secs, logtext))
                print("Log ({0}): {1}".format(self.stopWatch.value_secs, logtext), file=sys.stderr)

        if len(self.displayedEvents) == 4:
            self.displayedEvents.pop(0)

        self.displayedEvents.append(str(text)[:13])
        self.display.clear()
        for i, event in enumerate(self.displayedEvents):
            self.display.draw.text((0,i*30), event, font=fonts.load('luBS24'))
        self.display.update()  

    def forwardCm(self, speed, distance, stop=True):
        degrees = distance * (360 / 17.6)
        self.forwardAngle(speed, degrees, stop)

    def forwardAngle(self, speed, degrees, stop=True):
        if stop: 
            if speed * degrees < 0:
                speed = abs(speed)           
                degrees = -abs(degrees)
            self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=Motor.STOP_ACTION_HOLD)
            self.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=Motor.STOP_ACTION_HOLD)
            self.left_motor.wait_until_not_moving()
            self.right_motor.wait_until_not_moving()

        if not stop:
            self.left_motor.position = 0
            self.right_motor.position = 0
            if speed * degrees < 0:
                self.left_motor.run_forever(speed_sp = -abs(speed))            
                self.right_motor.run_forever(speed_sp = -abs(speed))            
                while self.left_motor.position + self.right_motor.position > -2 * abs(degrees):
                    pass
            else:
                self.left_motor.run_forever(speed_sp = abs(speed))            
                self.right_motor.run_forever(speed_sp = abs(speed))            
                while self.left_motor.position + self.right_motor.position < 2 * abs(degrees):
                    pass

    def alignToNotWhite(self, speed, whiteThreshold = None):
        self.left_motor.run_forever(speed_sp = speed)            
        self.right_motor.run_forever(speed_sp = speed)            
        while (self.left_motor.is_running or self.right_motor.is_running):
            if (not self.leftColorSensor.isWhiteReflection(whiteThreshold)):
                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            if (not self.rightColorSensor.isWhiteReflection(whiteThreshold)):
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.stop()

    def turn(self, angle, speed=None, left_speed=None, right_speed=None, stop=True):  # pozitív angle -> jobbra
        angle=angle*1
        if speed != None:
            degrees = 270 * (angle / 90)
            self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=abs(speed), stop_action=Motor.STOP_ACTION_HOLD)
            self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=abs(speed), stop_action=Motor.STOP_ACTION_HOLD)
        elif left_speed != None:
            degrees = 580 * (angle / 90)
            self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=abs(left_speed), stop_action=Motor.STOP_ACTION_HOLD)
        elif right_speed != None:
            degrees = 580 * (angle / 90)
            self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=abs(right_speed), stop_action=Motor.STOP_ACTION_HOLD)
        else: 
            self.log("Attention! No speed given!")
        if stop:
            self.left_motor.wait_until_not_moving()
            self.right_motor.wait_until_not_moving()

    def checkColorAlign(self):
        self.leftColorSensor.mode = ColorSensor.MODE_RGB_RAW
        # self.rightColorSensor.mode = ColorSensor.MODE_RGB_RAW
        
        time.sleep(0.5)
        button = Button()
        while button.enter:
            time.sleep(0.3)
            self.log(self.leftColorSensor.rgb)
        self.leftColorSensor.mode = ColorSensor.MODE_REF_RAW
        self.rightColorSensor.mode = ColorSensor.MODE_REF_RAW
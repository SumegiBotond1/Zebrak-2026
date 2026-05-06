# pyright: reportMissingImports=false
# pyright: reportOptionalMemberAccess=false
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.console import Console
import sys
import ev3fast
class MyColorSensor(ColorSensor):

    def __init__(self, port):
        super().__init__(port)
        self.port = str(port).replace('ev-ports:', '')
        self.mode = ColorSensor.MODE_REF_RAW
        try:
            with open('color_values_{0}.txt'.format(self.port), 'r') as f:
                self.white_value = int(f.readline())
                self.black_value = int(f.readline())
        except:
            self.white_value = 422
            self.black_value = 622
            print('Calibration missing: {0}'.format(port), file=sys.stderr )            


    def getReflection(self):
        value = self.value()
        diff = self.black_value - self.white_value
        return int(((self.black_value - value) / diff) * 100)        

    def isBlackReflection(self, threshold = None):
        if threshold == None:
            threshold = 15
        reflection = self.getReflection()
        return  reflection <= threshold
    
    def isWhiteReflection(self, threshold = None):
        if threshold == None:
            threshold = 85
        return self.getReflection() >= threshold

    def isRed(self):
        r, g, b = self.rgb
        return r > 100 and g < 80 and b < 80
    
    def isNotRed(self):
        return not self.isRed()
    
    def isNotBlackReflection(self, threshold = None):
        return not self.isBlackReflection(threshold)
    
    def isNotWhiteReflection(self, threshold = None):
        return not self.isWhiteReflection(threshold)

    def calibrate(self, console = None):
        button = Button()
        # while not button.enter:
            # pass

        if console == None:
            console = Console()
        console.text_at(text="White", column=0, row=0, reset_console=True )

        Sound().speak('White')
        while not button.enter:
            pass
        white_value = self.value()

        console.text_at(text="Black", column=0, row=0, reset_console=True )
        Sound().speak('Black')
        while not button.enter:
            pass
        black_value = self.value()

        with open('color_values_{0}.txt'.format(self.port), 'w') as f:
            f.write('{0}\n'.format(white_value))
            f.write('{0}\n'.format(black_value))

        print('White: {0}, Black: {1}'.format(white_value, black_value), file=sys.stderr )

    def get_modes(self):
        # The path of the modes file.
        modes_path = self.modes

        # Open the modes file.
        with open(modes_path, 'r') as m:

            # Read the contents.
            contents = m.read()

            # Strip the newline symbol, and split at every space symbol.
            return contents.strip().split(' ')            

class MyGyroSensor:
    def __init__(self, port) -> None:
        self.gyro = ev3fast.GyroSensor(address= port)
        self.correction = 0
        self.offset = 0

    def reset_with_angle(self, now_angle):
        self.offset = -now_angle - self.gyro.angle

    def reset(self):
        self.correction = -self.gyro.angle
        self.offset = 0

    @property
    def angle(self):
        return self.gyro.angle + self.correction + self.offset
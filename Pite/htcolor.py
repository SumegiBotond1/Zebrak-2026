# pyright: reportMissingImports=false
# pyright: reportOptionalMemberAccess=false
from ev3dev2.sensor.lego import Sensor
import sys
class HTColor(Sensor):

    def __init__(self, port):
        address = port + ':i2c1'
        # print(address, file=sys.stderr)
        super().__init__(address)
        self.mode = 'COLOR'

    def color(self) -> int: return self.value(0)

    def rgbw(self):
        return (self.value(0), self.value(1), self.value(2), self.value(3))
        
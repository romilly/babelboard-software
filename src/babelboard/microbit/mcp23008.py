"""
Control an MCP23008 Port expander via I2C

See https://www.microchip.com/wwwproducts/en/MCP23008
This implements a subset of chip features to keep file size low.
"""

from microbit import *
import struct
from time import sleep

class MCP23008:
    IODIR = 0x00
    IPOL =  0x01
    GPPU =  0x06
    GPIO =  0x09

    def __init__(self, addr=None):
        self._addr = addr if addr else 0x20

    def _write(self, reg, value):
        i2c.write(self._addr,struct.pack('<BB', reg, value))

    def _read(self, reg):
        i2c.write(self._addr, struct.pack('<B', reg), repeat=True)
        return i2c.read(self._addr, 1)

    def output(self, val):
        self._write(self.GPIO, val)

    def input(self):
        return self._read(self.GPIO)

    def direction(self, val):
        self._write(self.IODIR, val)

    def gppu(self, val):
        self._write(self.GPPU, val)


def loop():
    ic = MCP23008()
    ic.direction(0x00)
    while True:
        for i in range(256):
            ic.output(i)
            sleep(0.1)


if __name__ == '__main__':
    loop()
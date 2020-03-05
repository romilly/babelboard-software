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
        """
        Initialise the object and chip.

        :param addr: I2C address (default set below to 0x20)
        """
        self._addr = addr if addr else 0x20
        self.ipol(0x000) # set normal polarity

    def _write(self, reg, value):
        i2c.write(self._addr,struct.pack('<BB', reg, value))

    def _read(self, reg):
        i2c.write(self._addr, struct.pack('<B', reg), repeat=True)
        return i2c.read(self._addr, 1)

    def output(self, val):
        """
        set output byte
        :param val: value to output
        :return:
        """
        self._write(self.GPIO, val)

    def input(self):
        """
        read input byte
        :return: chip inputs
        """
        return self._read(self.GPIO)

    def direction(self, val):
        """
        Set direction of pins.

        0 means pin is an input, 1 is an output
        Each pin is a bit in val; MSB=P7, lsb=P0
        :param val:
        :return:
        """
        self._write(self.IODIR, val)

    def gppu(self, val):
        self._write(self.GPPU, val)

    def ipol(self, val):
        self._write(self.IPOL, val)

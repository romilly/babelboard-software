from microbit import *
import struct
from time import sleep


class MCP23S08:
    GPIO = 0x09
    def __init__(self, addr=0x20):
        self._addr = addr

    def write(self, reg, value):
        pin16.write_digital(0) # Chip select
        spi.write(struct.pack('<BBB', self._addr << 1, reg, value))
        pin16.write_digital(1) # Chip select off

    def read(self, reg):
        pin16.write_digital(0) # Chip select
        spi.write(struct.pack('<BB',0x01 | self._addr << 1, reg))
        result = spi.read(1)
        pin16.write_digital(1) # Chip select off
        return result

    def iomode(self, val):
        self.write(0x00, val)

    def iopol(self, val):
        self.write(0x01, val)

    def output(self, val):
        self.write(0x09, val)

    def input(self):
        return self.read(0x09)

    def gppu(self, val):
        self.write(0x06, val)

def run():
    pin16.write_digital(1)
    spi.init()
    mcp = MCP23S08()
    mcp.iomode(0x0F)
    mcp.iopol(0x00)
    mcp.gppu(0x0f) # weak pull-ups on inputs
    map = [{1:'D', 2:'C', 4:'B', 8:'A'},{1:'#', 2:'9', 4:'6', 8:'3'},{1:'0', 2:'8', 4:'5', 8:'2'},{1:'*', 2:'7', 4:'4', 8:'1'}]
    while True:
        for i in range(4):
            op = 16 << i
            mcp.output(0xF0 ^ op) # flip output bits
            ip = 0x0F ^ ord(mcp.input()) # flip input bits
            b = ip % 16
            d = map[i]
            # print (i, ip, b)
            if b in d:
                print('char:', d[b])
            sleep(0.1)
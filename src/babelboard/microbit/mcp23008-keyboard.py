from microbit import *
import struct
from time import sleep


class MCP23008:
    IODIR = 0x00
    IPOL = 0x01
    GPPU = 0x06
    GPIO = 0x09
    def __init__(self, addr=0x20):
        self._addr = addr

    def write(self, reg, value):
        i2c.write(self._addr,struct.pack('<BB', reg, value))

    def read(self, reg):
        i2c.write(self._addr, struct.pack('<B', reg), repeat=True)
        return i2c.read(self._addr, 1)

    def prepare(self):
        self.write(self.IODIR, 0x0F)
        self.write(self.IPOL, 0x00) # Normal polarity
        self.write(self.GPPU, 0x0F) # weak pull-ups

    def output(self, val):
        self.write(self.GPIO, val)

    def input(self):
        return self.read(self.GPIO)

def run():
    mcp = MCP23008()
    mcp.prepare()
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
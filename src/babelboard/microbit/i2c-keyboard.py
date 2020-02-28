from microbit import *
from time import sleep


class Keyboard:
    def __init__(self, addr=0x08):
        self._addr = addr

    def read_char(self):
        return i2c.read(self._addr, 1)



def run():
    kbd = Keyboard()
    while True:
        key = kbd.read_char()
        if (key != b'\x00'):
            print(key)
        sleep(0.01)

run()
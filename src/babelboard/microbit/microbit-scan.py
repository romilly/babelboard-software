from microbit import *

addrs = i2c.scan()
for addr in addrs:
    print(addr)
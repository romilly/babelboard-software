#!/usr/bin/env python3
import smbus
import time


# ADC121C021 address: Grove ADC 1.1 is at 0x55
GROVE_ADC_1_1_ADDR = 0x55
CONFIG_REG = 0x02
RESULT_REG = 0x00


def get_12_bit_data(data):
    return (data[0] & 0x0F) * 256 + data[1]


def read_adc():
    return get_12_bit_data(bus.read_i2c_block_data(GROVE_ADC_1_1_ADDR, RESULT_REG, 2))


def write_reg(register, value):
    bus.write_byte_data(GROVE_ADC_1_1_ADDR, register, value)


bus = smbus.SMBus(1)
write_reg(CONFIG_REG, 0x20) #	0x20 = Automatic conversion, 27k samples/sec

while True:
    time.sleep(0.5)
    adc = read_adc()
    print("Analog Input : %d" %adc)


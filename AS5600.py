import smbus
import time

class AS5600:
    def __init__(self, i2c_dev):
        self.address = 0x36
        self.raw_reg = 0x0c
        self.angle_reg = 0x0d
        self.i2c = i2c_dev
    def read_angle(self):
        data = self.i2c.read_word_data(self.address, self.angle_reg)
        print(round(data/4096*360, 2))

bus = smbus.SMBus(1)
as5600 = AS5600(bus)
while(1):
    as5600.read_angle()
    time.sleep(1)

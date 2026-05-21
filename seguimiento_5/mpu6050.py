from machine import I2C

class MPU6050:

    def __init__(self, i2c, addr=0x68):

        self.i2c = i2c
        self.addr = addr

        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def read_raw_data(self, reg):

        high = self.i2c.readfrom_mem(self.addr, reg, 1)[0]
        low = self.i2c.readfrom_mem(self.addr, reg + 1, 1)[0]

        value = (high << 8) | low

        if value > 32768:

            value = value - 65536

        return value

    def read_accel_data(self):

        ax = self.read_raw_data(0x3B) / 16384.0
        ay = self.read_raw_data(0x3D) / 16384.0
        az = self.read_raw_data(0x3F) / 16384.0

        return {

            'x': ax,
            'y': ay,
            'z': az

        }
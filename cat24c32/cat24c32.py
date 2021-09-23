import smbus2
import time

_address = 0x50

class CAT24C32:
    def __init__(self, bus=0):
        self._bus = smbus2.SMBus(bus)

    def write(self, register_address, data):
        data = list(register_address.to_bytes(2, "big")) + data
        msg = smbus2.i2c_msg.write(_address, data)

        try:
            self._bus.i2c_rdwr(msg)
            return
        except OSError as e:
            if e.errno is 121: # Remote I/O error aka slave NAK
                pass

        time.sleep(0.005)
        self._bus.i2c_rdwr(msg)

    def read(self, register_address, length=1):
        self.write(register_address, [])
        msg = smbus2.i2c_msg.read(_address, length)
        self._bus.i2c_rdwr(msg)
        data = list(msg)
        return data

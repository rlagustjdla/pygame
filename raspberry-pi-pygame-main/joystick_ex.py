import smbus
import time

address = 0x48
A0 = 0x40
A1 = 0x41
bus = smbus.SMBus(1)

while True:
    bus.write_byte(address, A0)
    time.sleep(0.01)
    # up down
    value1 = bus.read_byte(address)
    
    bus.write_byte(address, A1)
    time.sleep(0.01)
    # left right
    value2 = bus.read_byte(address)
    
    print(value1, value2)
    time.sleep(0.1)

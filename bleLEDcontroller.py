# Adapted from: Tony DiCola
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import random
import struct
from time import sleep


ble = Adafruit_BluefruitLE.get_provider()
LEDCOUNT = 14


def main():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()
                    
    try:
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        while(True):
            n = randbyte(0, LEDCOUNT)
            r = randbyte(0, 256)
            g = randbyte(0, 256)
            b = randbyte(0, 256)
            s = b'n'+n+b'r'+r+b'g'+g+b'b'+b+b'\r'+b'\n'
            print(s)
            uart.write(s)
            sleep(1)

        print('Waiting up to 60 seconds to receive data from the device...')
    finally:
        device.disconnect()

def randbyte(low, high):
    return struct.pack('B',random.randrange(low, high))


ble.initialize()
ble.run_mainloop_with(main)

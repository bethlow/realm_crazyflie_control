"""
Scans for any crazyradio USB device connected to computer and
returns status and address of device, with option for serial number
"""
import logging
import time
from cflib.crtp.radiodriver import crazyradio

def crazyradio_scan(serial=False):

    print("Scanning for Crazyradio devices...")
    time.sleep(0.1)
    usb = crazyradio._find_devices()
    print("Devices:", usb)

    if serial:
        print("Getting serial numbers...")
        print(crazyradio.get_serials())

if __name__=='__main__':
    crazyradio_scan()
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def simple_connect():
    print("Connection!!! :P")
    time.sleep(10)
    print("Time to disconnect :(")

if __name__=='__main__':
    # Initiaize the drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cach='./cache')) as scf:
        simple_connect()

    

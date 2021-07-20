"""
Basic script for connecting and logging to crazyflie 
Based on tutorial from bitcraze.io -> 
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E701')
# Only output errors from logging
logging.basicConfig(level=logging.ERROR)

def simple_log(scf, logconf):
    with SyncLogger(scf, lg_stab) as logger:
        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))

            break

def simple_connect():
    print("Connection!!! :P")
    time.sleep(10)
    print("Time to disconnect :(")




if __name__=='__main__':
    # Initiaize the drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')
    
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        simple_log(scf, lg_stab)

    

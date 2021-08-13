"""
Logging of each available/connected crazyflie's battery levels
"""
import logging
import cflib.crtp
import time

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

def batt_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(battery_callback)

    logconf.start()
    time.sleep(1)
    logconf.stop()

def battery_callback(timestamp, data, logconf):
    print("Starting battery level: %s" %data, "%")
    # print('[%d][%s]: %s' % (timestamp, logconf.name, data))

def get_battery_status(uri):
    """
    Outputs log of battery status continuously for 
    all connected crazyflies, where uris is the list
    of connected cf addresses
    """
    logging.basicConfig(level=logging.ERROR)
    cflib.crtp.init_drivers()

    lg_battery = LogConfig(name='batteryLevel', period_in_ms=500)
    lg_battery.add_variable('pm.batteryLevel', 'float')
    
    
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        batt_log_async(scf, lg_battery) 
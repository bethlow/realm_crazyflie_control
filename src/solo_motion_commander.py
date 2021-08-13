"""
Simple script for server/client flying of the crazyflie
"""

import logging
import time
from cflib.crazyflie.commander import Commander

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E708')

DEFAULT_HEIGHT = 0.5
BOX_LIMIT = 0.5

is_deck_attached = False
is_cf_charged = True
logging.basicConfig(level=logging.ERROR)

position_estimate = [0, 0, 0]

def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)


def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.stop()
   
def take_off_high(scf):
    with MotionCommander(scf, default_height=1.0) as mc:
        time.sleep(1)
        # mc.stop()
        # time.sleep(1)
        mc.circle_left(0.2)
        time.sleep(1)

def move_circle(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.circle_left(0.2)
        time.sleep(1)
        # mc.stop()
        # time.sleep(1)

def commander_take_off(cf):
    with Commander(cf) as com:
        com.send_setpoint(0,0,0,30000)
        time.sleep(3)
        com.send_setpoint(0,0,0,0)

def log_pos_callback(timestamp, data, logconf):
    # print(data)
    global position_estimate
    global is_cf_charged
    
    position_estimate[0] = data['stateEstimateZ.x']
    position_estimate[1] = data['stateEstimateZ.y']
    position_estimate[2] = data['stateEstimateZ.z']

    print("-------------------------")
    print("Time: ", timestamp)
    print("Connected to crazyflie at URI: ", URI)
    print("                            x       y       z\n",
          "Crazyflie at position: ",  position_estimate)

    print("Current thrust: ", data['stabilizer.thrust'])
    print("Battery status: ", data['pm.batteryLevel'], "%")

    print("-------------------------")

def param_deck_lps(name, value_str):
    value = int(value_str)
    global is_deck_attached
    if value:
        is_deck_attached = True
        print('Deck %s (LPS) is attached!' %name)
    else:
        is_deck_attached = False
        print('Deck is NOT attached!')


if __name__ == '__main__':
    pass
    # cflib.crtp.init_drivers()

    # with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

    #     scf.cf.param.add_update_callback(group='deck', name='bcDWM1000',
    #                                      cb=param_deck_lps)
    #     time.sleep(1)

    #     logconf = LogConfig(name='Position', period_in_ms=500)
    #     logconf.add_variable('stateEstimateZ.x', 'float')
    #     logconf.add_variable('stateEstimateZ.y', 'float')
    #     logconf.add_variable('stateEstimateZ.z', 'float')
    #     logconf.add_variable('pm.batteryLevel', 'float')
    #     logconf.add_variable('stabilizer.thrust', 'float')
    #     scf.cf.log.add_config(logconf)
    #     logconf.data_received_cb.add_callback(log_pos_callback)

    #     if is_deck_attached:
    #         logconf.start()

    #         take_off_simple(scf)
    #         # take_off_high(scf)
    #         # move_circle(scf)
    #         # move_linear_simple(scf)

    #         logconf.stop()
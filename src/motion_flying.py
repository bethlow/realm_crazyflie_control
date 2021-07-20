"""
Simple script for server/client flying of the crazyflie
"""

import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

from cflib.crazyflie.log import LogConfig

URI1 = 'radio://0/80/2M/E7E7E7E708'
DEFAULT_HEIGHT = 0.5

is_deck_attached = False

logging.basicConfig(level=logging.ERROR)

position_estimate = [0, 0]

def take_off_simple(scf):
    with MotionCommander(scf) as mc:
        mc.up(0.3)
        time.sleep(3)

def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        # mc.back(0.8)
        # time.sleep(1)
        mc.circle_left(0.2)
        time.sleep(1)

def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']

def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    global is_deck_attached
    if value:
        is_deck_attached = True
        print('Deck is attached!')
    else:
        is_deck_attached = False
        print('Deck is NOT attached!')


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        # scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
        #                                  cb=param_deck_flow)
        # time.sleep(1)

        # if is_deck_attached:
        logconf = LogConfig(name='Position', period_in_ms=100)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        # if is_deck_attached:
        logconf.start()

        move_linear_simple(scf)

        logconf.stop()


        # take_off_simple(scf)


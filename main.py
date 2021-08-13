"""
Main control script for flying one or multiple Crazyflies, 
using functions from the cflib. 
Connects to available URIs and runs basic flight maneuvers
from the motion commander in the cflib, successively, 
in numerical order by ID of the crazyflie.

Can be programmed to run concurrently, using threads.
"""
from cflib import crazyflie
from cflib.crazyflie.log import Log, LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
import cflib.crtp
from cflib.crazyflie import Crazyflie
from threading import Thread
import time
import logging
from src.scan import scan
from src.battery_status import get_battery_status
import src.solo_motion_commander as mc

logging.basicConfig(level=logging.ERROR)

class Main:
    """Class for setting up initial logging and connection
    to available crazyflies"""
    def __init__(self, link_uri):

        self._cf = Crazyflie(rw_cache='./cache')

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        self.connected = True

        print('Connecting to %s' % link_uri)
    
    def _connected(self, link_uri):
        """ This callback is called from the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print("Crazyflie connected at %s" %link_uri)
        # Thread(target=self.ramp_motors).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))
        self.connected = False

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.connected = False


    def ramp_motors(self, thrust):
        """
        params: thrust - float value of desired thrust
        Ramps the motors up to specified thrust, then back to zero
        """
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        self._cf.commander.send_setpoint(0, 0, 0, thrust)
        time.sleep(1)
        self._cf.commander.send_setpoint(0,0,0,10000)
        time.sleep(0.1)
        self._cf.commander.send_setpoint(0,0,0,0)

        time.sleep(0.1)
        self._cf.close_link()

    


if __name__=='__main__':
    # Comment out unused addresses as necessary
    # All addresses listed here are available in the REALM lab
    address_list = [
        0xE7E7E7E701,
        0xE7E7E7E702,
        # 0xE7E7E7E703,
        # 0xE7E7E7E704,
        # 0xE7E7E7E705,
        # 0xE7E7E7E706,
        # 0xE7E7E7E707,
        # 0xE7E7E7E708,
        # 0xE7E7E7E709,
        # 0xE7E7E7E70A,
    ]

    # Initialize the drivers
    cflib.crtp.init_drivers()
    # Scan each cf address for list of available connections
    uris = scan(address_list)
    time.sleep(1)

    # Run sequence of cf commands for each available drone  
    for uri in uris:
        print("*********************")
        print("URI: " + uri)
        get_battery_status(uri)
        print("*********************")
        time.sleep(0.5)

        if len(uris) == 0:
            print("No crazyflies available for connection")
            break
        
        # Initializing syncronous instance of crazyflie
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            scf.cf.param.add_update_callback(group='deck', name='bcDWM1000',
                                            cb=mc.param_deck_lps)
            time.sleep(1)

            # Log configuration for current location, thrust, and battery status
            logconf = LogConfig(name='Position', period_in_ms=500)
            logconf.add_variable('stateEstimateZ.x', 'float')
            logconf.add_variable('stateEstimateZ.y', 'float')
            logconf.add_variable('stateEstimateZ.z', 'float')
            logconf.add_variable('pm.batteryLevel', 'float')
            logconf.add_variable('stabilizer.thrust', 'float')
            scf.cf.log.add_config(logconf)
            logconf.data_received_cb.add_callback(mc.log_pos_callback)

            # Make sure LPS deck is properly attached
            if mc.is_deck_attached:
                input(">>> Press enter to continue to flight command...")

                logconf.start()

                mc.take_off_simple(scf)
                ## Other crazyflie maneuvers, uncomment to use
                # mc.take_off_high(scf)
                # mc.move_circle(scf)
                # mc.move_linear_simple(scf)

                logconf.stop()

            



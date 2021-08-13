"""
Simple script that scans for available Crazyflies at a specified address
"""
from src.crazyradio_scan import crazyradio_scan
import cflib.crtp
import time

#Scan for the Crazyradio PA 
crazyradio_scan()

def scan(addresses=None):
    # Initiate the low level drivers
    cflib.crtp.init_drivers()

    print('Scanning interfaces for Crazyflies...')
    time.sleep(1)

    print('Crazyflies found:')
    cf_available = []

    if addresses!=None:
        for i in addresses:
            available = cflib.crtp.scan_interfaces(i)
            if len(available)==0:
                print("No interface found with URI [%s]" %i)

            # for j in available:
            else:
                print("Interface with URI [%s] found" % (available[0][0]))
                cf_available.append(available[0][0])
        
        print("List of all available Crazyflies:", cf_available)
        time.sleep(0.5)        
        print("Scan complete!")
        time.sleep(0.5)
    else:
        available = cflib.crtp.scan_interfaces()
        return available

    return cf_available
    
if __name__=='__main__':
    address_list = [
    0xE7E7E7E701,
    0xE7E7E7E702,
    0xE7E7E7E703,
    0xE7E7E7E704,
    0xE7E7E7E705,
    0xE7E7E7E706,
    0xE7E7E7E707,
    0xE7E7E7E708,
    0xE7E7E7E709,
    0xE7E7E7E70A,
    ]   

    scan(address_list)
    
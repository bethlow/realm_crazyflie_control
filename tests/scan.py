"""
Simple script that scans for available Crazyflies at specified address
"""
from crazyradio_scan import crazyradio_scan
import cflib.crtp
import time

crazyradio_scan()

# List of all possible cf addresses in REALM lab
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

def scan(addresses=None):
    # Initiate the low level drivers
    cflib.crtp.init_drivers()

    print('Scanning interfaces for Crazyflies...')
    time.sleep(0.1)

    print('Crazyflies found:')
    cf_available = []
    for i in addresses:
        available = cflib.crtp.scan_interfaces(i)
        if len(available)==0:
            print("No interface found with URI [%s]" %i)

        for j in available:
            print("Interface with URI [%s] found" % (j[0]))
            cf_available.append(j[0])
    
    print("List of all available Crazyflies:", cf_available)        
    print("Scan complete!")

    return cf_available
    
if __name__=='__main__':
    scan(address_list)
    
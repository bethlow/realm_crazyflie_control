#
#
"""
Basic control script for connecting to and flying one Crazyflie,
after scanning and selecting URI based on available cfs 
"""
from tests.scan import scan
uris = scan()

print(uris)
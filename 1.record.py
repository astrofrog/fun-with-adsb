# Simply record ADS-B messages - requires the rtl-sdr package to be installed
# This also searches specifically for messages with downlink format 17 (10001)

import time
import codecs
import subprocess

p = subprocess.Popen('rtl_adsb',
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

with codecs.open('plane_data.txt', 'w', encoding='ascii') as f:
    while True:
        timestamp = time.time()
        hex_data = p.stdout.readline().decode('ascii').strip()[1:-1]
        bin_data = "{0:0112b}".format(int(hex_data, 16))
        if bin_data[:5] == '10001':
            f.write("{0:.3f} {1}\n".format(timestamp, hex_data))
            f.flush()


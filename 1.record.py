#!/usr/bin/env python

# Simply record ADS-B messages - requires the rtl-sdr package to be installed
# This also searches specifically for messages with downlink format 17 (10001)

import os
import time
import subprocess

import pyModeS as pms

p = subprocess.Popen('rtl_adsb',
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

if not os.path.exists('raw'):
    os.mkdir('raw')

fout = None

while True:

    timestamp = time.time()
    hex_data = p.stdout.readline().decode('ascii').strip()[1:-1]

    # Make sure the message is valid using the checksum
    if int(pms.util.crc(hex_data), 2) != 0:
        continue

    bin_data = "{0:0112b}".format(int(hex_data, 16))

    if bin_data[:5] == '10001':

        filename = os.path.join('raw', str(int(timestamp / 100000)))

        if fout is not None and fout.name != filename:
            fout.close()
            fout = None

        if fout is None:
            fout = open(filename, 'w')

        fout.write("{0:.3f} {1}\n".format(timestamp, hex_data))
        fout.flush()

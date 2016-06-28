# Split the raw planes_data.txt file into one file per aircraft, and also
# filter out messages for which the checksum fails.

import os
from collections import defaultdict

import pyModeS as pms

data = defaultdict(list)

for i, line in enumerate(open('plane_data.txt')):

    if i % 1000 == 0:
        print("Processed {0} messages...".format(i))

    hex_data = line.strip().split()[1]

    # Find aircraft ID
    aircraft = pms.adsb.icao(hex_data)

    # Output only entries with a valid checksum
    if int(pms.util.crc(hex_data), 2) == 0:
        data[aircraft].append(line)

if not os.path.exists('raw'):
    os.mkdir('raw')

for aircraft in data:
    if len(data[aircraft]) > 10:
        with open(os.path.join('raw', aircraft), 'w') as f:
            for line in data[aircraft]:
                f.write(line)

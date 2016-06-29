import os
import sys
import glob
import multiprocessing as mp
from collections import defaultdict, Counter

import pyModeS as pms
from astropy.table import Table

counter = Counter()

lon_lat_cache = defaultdict(dict)

def process(filename):

    t = Table(names=('timestamp', 'longitude', 'latitude', 'altitude', 'ground_speed', 'air_speed', 'heading', 'vertical_rate'),
              dtype=(float, float, float, float, float, float, float, float), masked=True)


    callsigns = Counter()

    for line in open(filename):

        timestamp, hex_data = line.strip().split()
        timestamp = float(timestamp)

        bin_data = "{0:0112b}".format(int(hex_data, 16))

        # Downlink Format
        df = int(bin_data[:5], 2)

        # ItcO aircraft address
        aircraft = "{0:6x}".format(int(bin_data[8:32], 2))

        # Type code
        tc = int(bin_data[32:37], 2)

        row = {'timestamp': timestamp}

        if tc <= 4:  # Aircraft identification

            try:
                callsign = pms.adsb.callsign(hex_data).replace('_', '')
            except:
                pass
            else:
                callsigns[callsign] += 1
                continue

        elif 9 <= tc <= 18:  # Airborne position (Baro Alt)

            if bin_data[53] == '0':
                lon_lat_cache[aircraft]['even'] = (timestamp, hex_data)
            else:
                lon_lat_cache[aircraft]['odd'] = (timestamp, hex_data)

            if 'even' in lon_lat_cache[aircraft] and 'odd' in lon_lat_cache[aircraft]:

                t_e, msg_e = lon_lat_cache[aircraft]['even']
                t_o, msg_o = lon_lat_cache[aircraft]['odd']

                if abs(t_e - t_o) < 5:

                    result = pms.adsb.position(msg_e, msg_o, t_e, t_o)

                    if result is not None:
                        lat, lon = pms.adsb.position(msg_e, msg_o, t_e, t_o)
                        alt_e = pms.adsb.altitude(msg_e) * 0.3048 / 1000.

                        row['longitude'] = lon
                        row['latitude'] = lat
                        row['altitude'] = alt_e

        elif tc == 19:  # Airborne velocities

            speed, heading, vertical_rate, speed_type = pms.adsb.velocity(hex_data)
            if speed_type == 'GS':
                row['ground_speed'] = speed
            else:
                row['air_speed'] = speed
            row['heading'] = heading
            row['vertical_rate'] = vertical_rate

        else:
            continue

        t.add_row(row)

    # We only trust the callsign if it was received 5 times or more
    if len(callsigns.most_common()) >= 1:
        callsign, count = callsigns.most_common()[0]
        if count < 5:
            callsign = 'UNKNOWN'
    else:
        callsign = 'UNKNOWN'

    t.meta['CALLSIGN'] = callsign

    t.write(os.path.join('tables', aircraft + '.fits'), overwrite=True)

if not os.path.exists('tables'):
    os.mkdir('tables')

p = mp.Pool(processes=12)
list(map(process, glob.glob(os.path.join('raw', '*'))))

#!/usr/bin/env python

import os
import time

RAW_DIR = os.path.join(os.path.dirname(__file__), 'raw')

if not os.path.exists(RAW_DIR):
    os.mkdir(RAW_DIR)

fout = None

while True:

    timestamp = time.time()

    filename = os.path.join(RAW_DIR, str(int(timestamp / 100000)) + '_temp.log')

    if fout is not None and fout.name != filename:
        fout.close()
        fout = None

    if fout is None:
        fout = open(filename, 'a')

    temp = os.popen("vcgencmd measure_temp").readline()
    try:
        value_temperature = temp.replace("temp=","").replace("'C", "").strip()
    except Exception:
        continue

    fout.write("{0} {1}\n".format(time.time(), value_temperature))
    fout.close()

    time.sleep(10)

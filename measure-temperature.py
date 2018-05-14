import os
import time

RAW_DIR = os.path.join(os.path.dirname(__file__), 'raw')

if not os.path.exists(RAW_DIR):
    os.mkdir(RAW_DIR)

TEMPERATURE_FILE = os.path.join(RAW_DIR, 'temperature.log')

with open(TEMPERATURE_FILE, 'a') as fout:
    while True:
        temp = os.popen("vcgencmd measure_temp").readline()
        value_temperature = temp.replace("temp=","").replace("'C", "").strip()
        fout.write("{0} {1}\n".format(time.time(), value_temperature))
        time.sleep(10)

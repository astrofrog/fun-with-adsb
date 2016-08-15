# Split the raw planes_data.txt file into one file per aircraft, and also
# filter out messages for which the checksum fails.

import os
import sys
from collections import defaultdict
import multiprocessing as mp

import pyModeS as pms

if len(sys.argv) != 2:
    print("Usage: python {0} directory".format(sys.argv[0]))
    sys.exit(1)
else:
    directory = sys.argv[1]

data = defaultdict(list)

def validate(message):
    """
    Return True if the message is valid, False otherwise
    """
    return int(pms.util.crc(message), 2) == 0

# We process the messages in chunks of 100000 so that we can parallelize
# things inside these chunks.

p = mp.Pool()

CHUNK_SIZE = 100000

f = open(os.path.join(directory, 'plane_data.txt'))

end = False

while True:

    print("Processing next chunk of {0}".format(CHUNK_SIZE))

    # Read next chunk of lines
    print(" -> Reading")
    lines = []
    for i in range(CHUNK_SIZE):
        line = f.readline()
        if line == "":
            end = True
            break
        if '\x00' not in line:
            lines.append(line)

    # Extract hex data
    print(" -> Extracting hex data")
    hex_data = [line.strip().split()[1] for line in lines]

    # Validate these chunks
    # print(" -> Validating messages")
    # valid = p.map(validate, hex_data)

    # Extract aircraft codes
    print(" -> Determining aircrafts")
    aircraft = p.map(pms.adsb.icao, hex_data)

    # Keep track only of valid entries and split by aircraft
    print(" -> Splitting by aircraft")
    for i in range(len(lines)):
        data[aircraft[i]].append(lines[i])

    if end:
        break

if not os.path.exists(os.path.join(directory, 'raw')):
    os.mkdir(os.path.join(directory, 'raw'))

print("Writing to file")

for aircraft in data:
    if len(data[aircraft]) > 10:
        with open(os.path.join(directory, 'raw', aircraft), 'w') as f:
            for line in data[aircraft]:
                f.write(line)

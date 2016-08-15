import os
import glob

import numpy as np
from astropy.table import Table, vstack


def nan_interp(x, y):
    # keep = ~np.isnan(y)
    # return np.interp(x, x[keep], y[keep])
    valid = None
    first_pos = None
    first_valid = None
    y_new = y.copy()
    for i in range(len(y)):
        if np.isnan(y[i]):
            if valid is not None:
                y_new[i] = valid
        else:
            valid = y[i]
            if first_pos is None:
                first_pos = i
                first_valid = valid
    if first_valid is not None:
        for i in range(first_pos):
            y_new[i] = first_valid
    return y_new
            

if not os.path.exists('tables_interp'):
    os.mkdir('tables_interp')

for filename in glob.glob(os.path.join('tables', '*.fits')):
    
    print("Processing {0}".format(filename))

    t = Table.read(filename)
    for column in t.colnames:
        if column == 'timestamp':
            continue
        elif column == 'callsign':
            continue
        elif np.all(np.isnan(t[column])):
            continue
        else:
            t[column] = nan_interp(t['timestamp'], t[column])

    t.write(filename.replace('tables', 'tables_interp'))

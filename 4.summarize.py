import os
import glob

import numpy as np
from astropy.table import Table, vstack
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

t_all = []

for filename in glob.glob(os.path.join('tables', '*.fits')):

    print(filename)
    t = Table.read(filename)
    sub = t[~np.isnan(t['altitude'])]['timestamp', 'callsign', 'longitude', 'latitude', 'altitude']
    t_all.append(sub)

t_all = vstack(t_all)
t_all.write('summary.fits', overwrite=True)

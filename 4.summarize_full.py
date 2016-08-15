import os
import glob

import numpy as np
from astropy.table import Table, vstack
from astropy.time import Time

t_all = []

for filename in glob.glob(os.path.join('tables_interp', '*.fits')):

    print(filename)
    t = Table.read(filename)
    sub = t[~np.isnan(t['altitude'])]
    if len(sub) > 0:
        t_all.append(sub)

t_all = vstack(t_all)

# Compute date/time from timestamp
date = Time(t_all['timestamp'], format='unix').plot_date
print(np.min(date))
date -= np.floor(np.min(date))

time = date % 1

t_all['date'] = date

t_all['time'] = time * 24 + 9


t_all.write('summary_full.fits', overwrite=True)

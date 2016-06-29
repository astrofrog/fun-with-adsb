import numpy as np
from astropy.table import Table
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

t = Table.read('summary.fits')

fig = plt.figure(figsize=(12,6))

ax = fig.add_subplot(1,1,1)

map = Basemap(projection='merc',llcrnrlat=50,urcrnrlat=55,\
              llcrnrlon=-7,urcrnrlon=2,lat_ts=52,resolution='c')

map.drawmapboundary(fill_color='#99ccff')

map.readshapefile('countries/countries', 'countries', drawbounds=False)

patches = []
for info, shape in zip(map.countries_info, map.countries):
    if info['NAME'] in ['United Kingdom', 'Ireland', 'France', 'Belgium', 'Luxembourg', 'Netherlands', 'Norway']:
        patches.append(Polygon(np.array(shape), True, facecolor='#ccffcc', edgecolor='none'))
        
ax.add_collection(PatchCollection(patches, zorder=2, match_original=True))

map.plot(t['longitude'], t['latitude'], 'k.', latlon=True, ax=ax, alpha=0.1, markersize=1)
map.plot(-1.5788031, 53.8164596, 'ro', latlon=True, markersize=5, alpha=0.5)

fig.savefig('uk_map.png', bbox_inches='tight', dpi=150)


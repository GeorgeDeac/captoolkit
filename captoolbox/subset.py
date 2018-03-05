import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

lon1, lon2 = -170, -95  # Amundsen Sea sector
#lon1, lon2 = -95, 0  # Drawning Maud sector
lat1 = -80

fname = sys.argv[1]

fi = h5py.File(fname, 'r')

lon = fi['lon'][:]
lat = fi['lat'][:]

idx, = np.where( (lon > lon1) & (lon < lon2) & (lat > lat1) )

fields = ['lon', 'lat', 'h_res', 't_year', 't_sec', 'bs', 'lew', 'tes']

with h5py.File(fname+'_subset', 'w') as fo:
    for var in fields:
        fo[var] = fi[var][:][idx]

fi.close()

import pandas as pd
from distars import healpix_index
from cdshealpix import lonlat_to_healpix, healpix_to_lonlat
from astropy.coordinates import Longitude, Latitude

df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')

ipix = healpix_index(df['source_id'].values, level=12)


# center of each pixel
ra_c, dec_c = healpix_to_lonlat(ipix=ipix, depth=12)
print('ra :',ra_c.deg)
print('dec:',dec_c.deg)

"""
# array of cells at different depths
ipix = np.array([42, 6, 10])
depth = np.array([12, 20])
"""

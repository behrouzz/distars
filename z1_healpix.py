import pandas as pd
from distars import sourceid_to_ipix
from cdshealpix import lonlat_to_healpix, healpix_to_lonlat
from astropy.coordinates import Longitude, Latitude

df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')


# Find pixel id (ipix) of each object
# -----------------------------------
ipix = sourceid_to_ipix(df['source_id'].values, level=12)

# For Gaia, we can find ipix directly from source_id (as we did above)
# But if we can also find ipix from ra & dec:

lon = Longitude(df['ra'].values, unit='deg')
lat = Latitude(df['dec'].values, unit='deg')
ipix_test = lonlat_to_healpix(lon, lat, depth=12)


# Find coordinates of center of each pixel (ra_c, dec_c)
# ------------------------------------------------------
ra_c, dec_c = healpix_to_lonlat(ipix=ipix, depth=12)
ra_c, dec_c = ra_c.deg, dec_c.deg

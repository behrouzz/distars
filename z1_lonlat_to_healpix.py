import pandas as pd
from distars import healpix_index
from cdshealpix import lonlat_to_healpix
from astropy.coordinates import Longitude, Latitude

df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')

lon = Longitude(df['ra'].values, unit='deg')
lat = Latitude(df['dec'].values, unit='deg')

ipix_kh = healpix_index(df['source_id'].values, level=12)
print(ipix_kh)
print()

ipix_cd = lonlat_to_healpix(lon, lat, depth=12)
print(ipix_cd)

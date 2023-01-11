import pandas as pd
import astropy.units as u
from astropy.coordinates import Longitude, Latitude
from cdshealpix import cone_search

# The Persian
ra, dec, r = 309.3918000320833, -47.2915007225, 1


ra = Longitude(ra, unit='deg')
dec = Latitude(dec, unit='deg')
r = r * u.deg

# Get the HEALPix cells contained in a cone at a given depth
# kh: ehtemalan default nested ast
# https://cds-astro.github.io/cds-healpix-python/api.html
ipix, depth, fully_covered = cone_search(lon=ra,
                                         lat=dec, 
                                         radius=r,
                                         depth=12)


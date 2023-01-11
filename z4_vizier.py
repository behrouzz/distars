import astropy.units as u
from astropy.coordinates import Longitude, Latitude, SkyCoord
from cdshealpix import cone_search
from mocpy import MOC
from astroquery.vizier import Vizier


ra, dec, r = 309.3918000320833, -47.2915007225, 1

ra = Longitude(ra, unit='deg')
dec = Latitude(dec, unit='deg')
r = r * u.deg

ipix, depth, fully_covered = cone_search(
    lon=ra, lat=dec, radius=r, depth=12
    )

# create moc
moc = MOC.from_healpix_cells(ipix=ipix,
                             depth=depth,
                             fully_covered=fully_covered)


cols = ['_RAJ2000', '_DEJ2000','B-V', 'Vmag', 'Plx']

viz = Vizier(columns=cols, column_filters={'Gmag': '<8'})
viz.ROW_LIMIT = -1

"""
# bad way : first downloads the whole catalog!
table = viz.get_catalogs('I/355/gaiadr3')[0]
a = table[moc]
"""

# directly query region
result = viz.query_region(SkyCoord(ra, dec, frame='icrs'),
                          radius=r,
                          catalog='I/355/gaiadr3',
                          )
table = rasult[0]

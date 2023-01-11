import astropy.units as u
from astropy.coordinates import Longitude, Latitude, SkyCoord, Angle
from regions import CircleSkyRegion
from astroquery.cds import cds

ra, dec, r = 309.3918000320833, -47.2915007225, 1

ra = Longitude(ra, unit='deg')
dec = Latitude(dec, unit='deg')
r = r * u.deg

cone = CircleSkyRegion(center=SkyCoord(ra,dec), radius=r)

cols = ['ID', 'dataproduct_type', 'moc_sky_fraction', 'moc_access_url']

tbl = cds.query_region(
    region=cone,
    #fields=cols
    ).to_pandas()


gaia = [i for i in tbl['ID'] if 'gaiadr3' in i]
gaia = tbl[tbl['ID'].isin(gaia)]
a = gaia.iloc[0]
print(a[a.notnull()])


# if we need the moc of gaiadr3:
#moc = cds.find_datasets(meta_data="CDS/I/355/gaiadr3", return_moc=True)

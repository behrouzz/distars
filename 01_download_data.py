from gaiadr3 import sql2df
from distars import in_radius

ra, dec, r = 309.3918000320833, -47.2915007225, 1

s = f"""SELECT
source_id, ra, dec,
parallax, distance_gspphot, pmra, pmdec,
radial_velocity, logg_gspphot,
phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag,
has_epoch_photometry
FROM gaiadr3.gaia_source
WHERE {in_radius(ra, dec, r)}
"""

df, _ = sql2df(s)

df.columns = [
    'source_id', 'ra', 'dec', 'plx', 'dist', 'pmra', 'pmdec',
    'radvel', 'surf_grav', 'g_mag', 'b_mag', 'r_mag', 'ep_phot'
    ]

df.set_index('source_id').to_csv('data/The_Persian_1deg_gaia3.csv')

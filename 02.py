from hypatie.simbad import sql2df
from distars import in_radius

ra, dec = 309.3918000320833, -47.2915007225
r = 1

s = f"""SELECT main_id, ra, dec, plx_value
FROM basic
WHERE plx_value IS NOT NULL AND
{in_radius(ra, dec, r)}
"""

df = sql2df(s)
#df.set_index('main_id').to_csv('data/The_Persian_1deg.csv')

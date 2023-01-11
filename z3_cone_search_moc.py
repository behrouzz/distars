import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import Longitude, Latitude, SkyCoord, Angle
from cdshealpix import cone_search
from mocpy import MOC, World2ScreenMPL

df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['g_mag']<10]

# The Persian
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


fig = plt.figure()

center = SkyCoord(ra, dec, frame='icrs')
fov = 3 * r
rot_ang = Angle(0, u.degree)

wcs = World2ScreenMPL(fig=fig,
                      fov=fov,
                      center=center,
                      coordsys="icrs",
                      rotation=rot_ang,
                      projection="AIT").w

ax = fig.add_subplot(1, 1, 1, projection=wcs)

ax.scatter(
    df['ra'].values,
    df['dec'].values,
    transform=ax.get_transform('icrs'),
    s=10, c='k',
    #edgecolor='red',
    #facecolor=(1, 1, 1, 0.5) # transparent white (0.5 is alpha)
    )

moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color="green")
moc.border(ax=ax, wcs=wcs, alpha=0.5, color="black") # perimeter of MOC

ax.coords[0].set_format_unit('deg', decimal=True)
ax.coords[1].set_format_unit('deg',decimal=True)
ax.set_aspect('equal')
plt.xlabel('ra')
plt.ylabel('dec')
plt.title('MOC with stars with G mag < 10')
plt.grid(color="black", linestyle="dotted")
plt.show()

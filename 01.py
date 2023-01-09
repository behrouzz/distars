from distars import simbad_count_circle

n = simbad_count_circle(
    ra=309.3918000320833,
    dec=-47.2915007225,
    radius=1,
    where='plx_value IS NOT NULL'
    )

print(n)

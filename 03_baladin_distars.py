import pandas as pd
from baladin import Aladin
from distars import gaia_distmat, nearest_pairs


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]
d = gaia_distmat(df, ['ra','dec','dist'])
pairs, dists = nearest_pairs(d, below=0.5)


ls = []
for i in range(len(pairs)):
    ind1, ind2 = pairs[i]
    ra1 = df.iloc[ind1]['ra']
    dec1 = df.iloc[ind1]['dec']
    name1 = df.iloc[ind1]['source_id']
    ra2 = df.iloc[ind2]['ra']
    dec2 = df.iloc[ind2]['dec']
    name2 = df.iloc[ind2]['source_id']
    dist = round(dists[i], 4)
    desc1 = f"Distance to {name2}: {dist} pc"
    desc2 = f"Distance to {name1}: {dist} pc"
    tuple1 = (ra1, dec1, name1, desc1)
    tuple2 = (ra2, dec2, name2, desc2)
    ls.append((tuple1, tuple2))


markers = [i for sublist in ls for i in sublist]

a = Aladin(target='309.3918000320833, -47.2915007225', fov=3)

buttons = [
    ('P/2MASS/color', 'bs 2MASS'),
    ('P/GLIMPSE360', 'bs GLIMPSE 360'),
    ]

a.add_survey_buttons(buttons)
a.add_markers(markers)
a.create()
a.save('index.html')

# for example:
aa = df[df['source_id'].isin([6482282509359112576, 6482282509359111680])]
print(aa.iloc[0])
print('-------------------------------------')
print(aa.iloc[1])

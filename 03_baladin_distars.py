import pandas as pd
from baladin import Aladin
from distars import gaia_distmat, nearest_pairs


def desc(df, ind1, ind2, dist_pair):
    s1 = ''
    for k,v in df.iloc[ind1].items():
        if k == 'source_id':
            source_id1 = v
            continue
        elif isinstance(v, float):
            value = str(round(v,4))
        else:
            value = str(v)
        s1 = s1 + k + ': ' + value + '<br/>'
    s2 = ''
    for k,v in df.iloc[ind2].items():
        if k == 'source_id':
            source_id2 = v
            continue
        elif isinstance(v, float):
            value = str(round(v,4))
        else:
            value = str(v)
        s2 = s2 + k + ': ' + value + '<br/>'
    s1 = s1 + f"<br/><em>Distance to {source_id2}:<em> {round(dist_pair,4)}<br/>"
    s2 = s2 + f"<br/><em>Distance to {source_id1}:<em> {round(dist_pair,4)}<br/>"
    return s1, s2


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]
#df = df[df['radvel'].notnull()]

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
    dist_pair = round(dists[i], 4)
    desc1, desc2 = desc(df, ind1, ind2, dist_pair)
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

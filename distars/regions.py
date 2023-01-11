import numpy as np
#from hypatie.transform import sph2car
from hypatie.simbad import sql2df as simbad_sql2df
from gaiadr3 import sql2df as gaia_sql2df


def in_radius(ra, dec, r):
    s = "CONTAINS(POINT('ICRS', ra, dec), " + \
        f"CIRCLE('ICRS', {ra}, {dec}, {r})) = 1"
    return s


def count(ra, dec, radius, database='gaia', where=None):
    
    if database.lower()[:4]=='gaia':
        table = 'gaiadr3.gaia_source'
        idcol = 'source_id'
    elif database.lower()=='simbad':
        table = 'basic'
        idcol = 'main_id'
    else:
        raise Exception('Database unknown!')
    
    where = '' if where is None else ' AND '+where
    s = f'SELECT COUNT({idcol}) AS num FROM {table} '
    s = s + f'WHERE {in_radius(ra, dec, radius)}' + where

    if database.lower()[:4]=='gaia':
        try:
            df,_ = gaia_sql2df(s)
            return df['num'].iloc[0]
        except:
            print('Error in retrieving from server! Try here:')
            print('https://gea.esac.esa.int/archive/\n')
            print(s)
            
    if database.lower()=='simbad':
        try:
            df = simbad_sql2df(s)
            return int(df['num'].iloc[0])
        except:
            print('Error in retrieving from server! Try here:')
            print('https://simbad.cds.unistra.fr/simbad/sim-tap\n')
            print(s)

def gaia_to_simbad(source_id):
    # ex: gaia_to_simbad(1870117138241890432)
    s1 = "SELECT b.main_id FROM ids AS i "
    s2 = "LEFT JOIN basic AS b ON b.oid=i.oidref "
    s3 = f"WHERE ids LIKE '%Gaia DR3 {source_id}%'"
    df = simbad_sql2df(s1+s2+s3)
    return df

import numpy as np
from hypatie.transform import sph2car
from hypatie.simbad import sql2df


def plx2car(df, col_names=['ra','dec','plx_value']):
    """
    Add cartesian position to a dataframe containing ra, dec and parallax

    It gets a dataframe and adds four columns to it: 'r', 'x', 'y', 'z'.
    The 'r' columns is the distance calculated from the parallax, and the
    other three columns are cartesian positions. All units are in parsec.

    Arguments
    ---------
        df        : dataframe
        col_names : columns names in dataframe for ra, dec and parallax

    Returns
    -------
        df : dateframe with four more columns: 'r', 'x', 'y', 'z'.
    """
    ra, dec, plx = col_names
    df['r'] = 1/(df[plx]/1000)
    pos_sph = df[[ra,dec,'r']].values
    pos_car = sph2car(pos_sph)
    df['x'], df['y'], df['z'] = pos_car.T
    return df


def create_hovertext(df):
    h = '<b>'+df['main_id'].str.replace('"','')+'</b><br>' + \
        'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str) + '<br>' \
        'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str) + '<br>'\
        'Distance: '+df['r'].apply(lambda x: round(x,3)).astype(str)+' <i>(pc)</i><br>' + \
        'Parallax: '+df['plx_value'].astype(str)+' <i>(mas)</i><br>'
    return h


def in_radius(ra, dec, r):
    s = "CONTAINS(POINT('ICRS', ra, dec), " + \
        f"CIRCLE('ICRS', {ra}, {dec}, {r})) = 1"
    return s


def simbad_count_circle(ra, dec, radius, where=None):
    where = '' if where is None else ' AND '+where
    s = 'SELECT COUNT(main_id) FROM basic '
    s = s + f'WHERE {in_radius(ra, dec, radius)}' + where
    df = sql2df(s)
    return int(df['COUNT'].iloc[0])
    

def dist_array_old(p):
    """Decrypted... use dist_array instead
    p : position cartesian matrix (NxN)
    d : distance matrix 
    """
    N = p.shape[0]
    d = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            d[i,j] = np.linalg.norm(np.array(p[i,:]-p[j,:]))
    for i in range(N): # to prevent 0s in diagonal
        #d[i,i] = round(d.max()+1,0)
        d[i,i] = 999999.0 # or np.nan
    return d


def dist_array(p):
    """Decrypted... use dist_array instead
    p : position cartesian matrix (NxN)
    d : distance matrix 
    """
    N = p.shape[0]
    d = np.zeros((N,N))
    rows, cols = np.diag_indices_from(d)
    for i in range(1,N):
        i_upper = (rows[:-i], cols[i:])
        d[i_upper] = np.linalg.norm(p[:-i]-p[i:], axis=1)
    i_lower = np.tril_indices(N, -1)
    d[i_lower] = d.T[i_lower]

    # temporary
    d[np.diag_indices_from(d)] = 999999.0 # or np.nan
    return d


def nearest_pairs(d, below=1):
    """
    Get pairs of stars which have distances less than a number (pc)
    
        d     : distance array
        below : condition; distances less than 'below' will be considered

    Returns
    -------
        pairs (list of 2d-sets) : pairs of stars (indexes)
        dists (list of floats)  : distances between each pair
    """
    c = np.array(np.where(d<below))
    n_satisfy = c.shape[1]

    pairs = []
    dists = []
    for i in range(n_satisfy):
        idx1 = c[0,i]
        idx2 = c[1,i]
        if not set((idx1, idx2)) in pairs:
            pairs.append(set((idx1, idx2)))
            dists.append(d[idx1, idx2])
    return pairs, dists

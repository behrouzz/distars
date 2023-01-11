import numpy as np
from hypatie.transform import sph2car


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





def distmat(p, diag_zero=True):
    """
    Distance Matrix

    Arguments
    ---------
        p (np.array) : position cartesian matrix (Nx3)

    Returns
    -------
        d (np.array) : distance matrix (NxN)
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
    if not diag_zero:
        d[np.diag_indices_from(d)] = 999999.0 # or np.nan
    return d


def gaia_distmat(df, coord_cols=['ra', 'dec', 'distance_gspphot']):
    ra, dec, dist = coord_cols
    has_ra = ra in df.columns
    has_dec = dec in df.columns
    has_dist = dist in df.columns
    if (has_ra and has_dec and has_dist):
        if df[dist].isnull().sum()==0:
            pos_car = sph2car(df[[ra, dec, dist]].values)
            d = distmat(pos_car, diag_zero=False)
            return d
        else:
            raise Exception('The distance column should not have NULL values')
    else:
        raise Exception('ra, dec, distance columns not indicated!')


def nearest_pairs(d, below=1):
    """
    Get pairs of stars which have distances less than a number (pc)

    Arguments
    ----------
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


def sourceid_to_ipix(source_id, level=12):
    """
    Healpix index/indices of Gaia object/(s) at desired level.

    Note: The approximate ICRS position is encoded using the nested HEALPix
    scheme at level 12 (Nside=4096), which divides the sky into ≃200 million
    pixels of about 0.7 arcmin2.
    """
    return (source_id / 2**(59-2*level)).astype(int)

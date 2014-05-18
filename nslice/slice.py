# -*- python -*-


import numpy as np

def slice(hklEIE, **kwds):
    """
    slice(hklEIE, x='h', y='E', k=[-0.1,0.1], l=[None,None])
    """
    xaxisname = kwds['x']
    yaxisname = kwds['y']
    return


def slice_hE(hklEIE, k=None, l=None, h=None, E=None):
    kmin,kmax = k
    lmin,lmax = l
    hmin, hmax, dh = h
    Emin, Emax, dE = E
    
    h, k, l, E, I, error = hklEIE
    data = hklEIE[:, (k>kmin)*(k<kmax)*(l>lmin)*(l<lmax)]
    
    I[I!=I] = 0 # remove nans in intensity
    sample = np.vstack((h, E)).T
    bins = [
        np.arange(hmin, hmax+dh/2, dh), 
        np.arange(Emin, Emax+dE/2, dE),
        ]
    weights = I
    H, edges = np.histogramdd(sample, bins=bins, weights=weights)
    return H, edges

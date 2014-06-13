# -*- python -*-


import numpy as np

def slice(hklEIE, x=None, y=None, u=None, v=None,
          h=None, k=None, l=None, E=None):
    """
    slice(hklEIE,
        x='h', y='E', u='k', v='l',
        k=[0.95,1.05], l=[-1,1],
        h=(-3, 5.8, 0.02), E=(-5, 10, 0.1),
        )
    """
    xmin, xmax, dx = eval(x)
    ymin, ymax, dy = eval(y)

    umin, umax = eval(u)
    vmin, vmax = eval(v)
    
    h, k, l, E, I, error = hklEIE
    data = hklEIE[:, (eval(u)>umin)*(eval(u)<umax)*(eval(v)>vmin)*(eval(v)<vmax)]
    h,k,l,E,I,error = data
    
    I[I!=I] = 0 # remove nans in intensity
    I[I<0] = 0
    sample = np.vstack((eval(x), eval(y))).T
    bins = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        ]
    weights = I
    H, edges = np.histogramdd(sample, bins=bins, weights=weights)
    return H, edges


def slice_output_dims(
    hklEIE, x=None, y=None, u=None, v=None,
    h=None, k=None, l=None, E=None):
    """
    slice_output_dims(hklEIE,
        x='h', y='E', u='k', v='l',
        k=[0.95,1.05], l=[-1,1],
        h=(-3, 5.8, 0.02), E=(-5, 10, 0.1),
        )
    """
    xmin, xmax, dx = eval(x)
    ymin, ymax, dy = eval(y)

    bins = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        ]
    return (bins[0].size-1, bins[1].size-1), bins


def slice_hE(hklEIE, k=None, l=None, h=None, E=None):
    kmin,kmax = k
    lmin,lmax = l
    hmin, hmax, dh = h
    Emin, Emax, dE = E
    
    h, k, l, E, I, error = hklEIE
    data = hklEIE[:, (k>kmin)*(k<kmax)*(l>lmin)*(l<lmax)]
    
    I[I!=I] = 0 # remove nans in intensity
    I[I<0] = 0
    sample = np.vstack((h, E)).T
    bins = [
        np.arange(hmin, hmax+dh/2, dh), 
        np.arange(Emin, Emax+dE/2, dE),
        ]
    weights = I
    H, edges = np.histogramdd(sample, bins=bins, weights=weights)
    return H, edges

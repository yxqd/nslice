# -*- python -*-


import numpy as np

def volume(hklEIE, x=None, y=None, z=None, u=None,
          h=None, k=None, l=None, E=None):
    """
    volume(hklEIE,
        x='h', y='k', z='E', u='l',
        k=(-4,4, 0.08), l=[-1,1],
        h=(-3, 6, 0.1), E=(-5, 10, 0.2),
        )
    """
    xmin, xmax, dx = eval(x)
    ymin, ymax, dy = eval(y)
    zmin, zmax, dz = eval(z)
    
    urange = eval(u)
    if urange is None: urange = None, None
    umin, umax = urange
    
    h, k, l, E, I, error = hklEIE
    limits = True
    if umin is not None: limits *= eval(u) > umin
    if umax is not None: limits *= eval(u) < umax
    # limits *= (eval(x) > xmin) * (eval(x) < xmax)
    # limits *= (eval(y) > ymin) * (eval(y) < ymax)
    # limits *= (eval(z) > zmin) * (eval(z) < zmax)
    
    if type(limits) is np.ndarray:
        data = hklEIE[:, limits]
        h,k,l,E,I,error = data    
    
    I[I!=I] = 0 # remove nans in intensity
    I[I<0] = 0
    sample = np.vstack((eval(x), eval(y), eval(z))).T
    bins = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        np.arange(zmin, zmax+dz/2, dz),
        ]
    weights = I
    H, edges = np.histogramdd(sample, bins=bins, weights=weights)
    return H, edges


def volume_output_dims(
    hklEIE, x=None, y=None, z=None, u=None,
    h=None, k=None, l=None, E=None):
    """
    volume_output_dims(hklEIE,
        x='h', y='E', z='k', v='l',
        k=[-3,4,0.03], l=[-1,1],
        h=(-3, 5.8, 0.02), E=(-5, 10, 0.1),
        )
    """
    xmin, xmax, dx = eval(x)
    ymin, ymax, dy = eval(y)
    zmin, zmax, dz = eval(z)
    
    bins = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        np.arange(zmin, zmax+dz/2, dz),
        ]
    return (bins[0].size-1, bins[1].size-1, bins[2].size-1), bins



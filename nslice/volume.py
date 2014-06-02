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
    
    umin, umax = eval(u)
    
    h, k, l, E, I, error = hklEIE
    data = hklEIE[:, (eval(u)>umin)*(eval(u)<umax)]
    
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
        x='h', y='k', z='E', u='l',
        k=(-4,4, 0.08), l=[-1,1],
        h=(-3, 6, 0.1), E=(-5, 10, 0.2),
        )
    """
    xmin, xmax, dx = eval(x)
    ymin, ymax, dy = eval(y)
    zmin, zmax, dz = eval(z)

    edges = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        np.arange(zmin, zmax+dz/2, dz),
        ]
    return (edges[0].size-1, edges[1].size-1, edges[2].size-1), edges



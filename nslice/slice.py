# -*- python -*-


import numpy as np

def slice(
    hklEIE, x=None, y=None, u=None, v=None,
    h=None, k=None, l=None, E=None,
    xaxis=None, yaxis=None, uaxis=None, vaxis=None,
    ):
    """
    slice(hklEIE,
        x='h', y='E', u='k', v='l',
        k=[0.95,1.05], l=[-1,1],
        h=(-3, 5.8, 0.02), E=(-5, 10, 0.1),
        )
    slice(hklEIE,
        x='100', y='E', u='010', v='001',
        uaxis=[0.95,1.05], vaxis=[-1,1],
        xaxis=(-3, 5.8, 0.02), yaxis=(-5, 10, 0.1),
        )
    """
    # x, y axes (min, max, delta)
    if x in 'hklE' and x in locals():
        xmin, xmax, dx = eval(x)
    else:
        xmin, xmax, dx = xaxis
    if y in 'hklE' and y in locals():
        ymin, ymax, dy = eval(y)
    else:
        ymin, ymax, dy = yaxis
    
    # u, v range
    # u
    if u in 'hklE' and u in locals():
        urange = eval(u)
    else:
        urange = uaxis
    if urange is None: urange = None, None
    umin, umax = urange
    # v
    if v in 'hklE' and v in locals():
        vrange = eval(v)
    else:
        vrange = vaxis
    if vrange is None: vrange = None, None
    vmin, vmax = vrange
    
    # get data
    h, k, l, E, I, error = hklEIE
    
    # get data for each axis
    xdata,ydata,udata,vdata = getData(x,y,u,v, h,k,l,E)
    del h,k,l,E, hklEIE
    
    #
    limits = True
    if umin is not None: limits *= udata > umin
    if umax is not None: limits *= udata < umax
    if vmin is not None: limits *= vdata > vmin
    if vmax is not None: limits *= vdata < vmax
    if type(limits) is np.ndarray:
        xdata = xdata[limits]
        ydata = ydata[limits]
        I = I[limits]
        error = error[limits]
        
    I[I!=I] = 0 # remove nans in intensity
    I[I<0] = 0
    sample = np.vstack((xdata, ydata)).T
    bins = [
        np.arange(xmin, xmax+dx/2, dx),
        np.arange(ymin, ymax+dy/2, dy),
        ]
    weights = I
    H, edges = np.histogramdd(sample, bins=bins, weights=weights)
    return H, edges


def getData(x,y,u,v, h,k,l,E):
    # map name to array
    name2arr = {}
    
    # one of the x y u v is 'E'
    names = ['x', 'y', 'u', 'v']
    # qaxes will be sth like [ ('x', 'h'), {'y', '001'}, ...]
    qaxes = []
    for name in names:
        if eval(name) == 'E': name2arr[name] = E; continue
        qaxes.append( (name, eval(name)) )
        continue
    #
    c2v = {'h': [1,0,0], 'k': [0,1,0], 'l': [0,0,1]}
    def tovector(axis):
        v = c2v.get(axis)
        if v: return v
        if isinstance(axis, basestring):
            if len(axis)==3: 
                return map(float, axis)
            axis = axis.split(',')
            return map(float, axis)
        return map(float, axis)
    # qaxes will be sth like [('x', [1,0,0]), ...]
    qaxes = [ (name, tovector(axis)) for name, axis in qaxes]
    # rotation matrix
    M = np.array([v for n, v in qaxes])
    M = np.linalg.inv(M.T)
    # compute coordinates in the new projection coordinate system
    x1,y1,z1 = np.dot(M, np.array([h,k,l]))
    name2arr[qaxes[0][0]] = x1
    name2arr[qaxes[1][0]] = y1
    name2arr[qaxes[2][0]] = z1
    return name2arr['x'], name2arr['y'], name2arr['u'], name2arr['v']


def slice_output_dims(
    hklEIE, x=None, y=None, u=None, v=None,
    h=None, k=None, l=None, E=None,
    xaxis=None, yaxis=None, uaxis=None, vaxis=None,
    ):
    """
    slice_output_dims(hklEIE,
        x='h', y='E', u='k', v='l',
        k=[0.95,1.05], l=[-1,1],
        h=(-3, 5.8, 0.02), E=(-5, 10, 0.1),
        )
    """
    if x in 'hklE' and x in locals():
        xmin, xmax, dx = eval(x)
    else:
        xmin, xmax, dx = xaxis
    if y in 'hklE' and y in locals():
        ymin, ymax, dy = eval(y)
    else:
        ymin, ymax, dy = yaxis
        
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

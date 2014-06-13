#!/usr/bin/env python

import os, numpy as np

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp/spe")

def process(path):
    basename, ext = os.path.splitext(os.path.basename(path))
    
    from nslice.Run import Run
    run = Run(path)
    print "file=%s, instrument=%s, Ei=%s, psi=%s" % (
        path, run.instrument, run.Ei, run.psi)

    from nslice.XtalOrientation import XtalOrientation
    a = b = 8.87;  c = 5.2
    from math import pi
    twopi = 2*pi
    ra,rb,rc = [twopi/a, 0,0], [0,twopi/b,0], [0,0,twopi/c]
    u,v = [1,0,0], [0,1,0]
    xtal_ori = XtalOrientation(ra,rb,rc, u,v, run.psi)

    h,k,l,E = run.compute_hklE(xtal_ori)
    I, error = run.read_data()
    h.shape = k.shape = l.shape = E.shape = I.shape = error.shape = -1
    hklEIE = np.vstack((h,k,l,E,I,error))
    
    from nslice.slice import slice
    H, edges = slice(
        hklEIE, 
        x = 'k', y = 'E', u = 'h', v = 'l',
        k=(-1,4,.03), E=(0,6,0.1), 
        h=(0.95,1.05), l=(-1,1),
        )
    
    solidangle_I = np.ones(h.shape, dtype='double')
    solidangle_error = np.zeros(h.shape, dtype='double')
    hklEIE = np.vstack((h,k,l,E,solidangle_I,solidangle_error))
    sa, edges = slice(
        hklEIE, 
        x = 'k', y = 'E', u = 'h', v = 'l',
        k=(-1,4,.03), E=(0,6,0.1), 
        h=(0.95,1.05), l=(-1,1),
        )
    return edges, H, sa


H = None; sa = None; edges = None
for i in range(28880, 29000):
    path = os.path.join(dir, "HYS_%d_4pixel.nxspe" % i)
    edges1, H1, sa1 = process(path)
    if H is None:
        edges, H, sa = edges1, H1, sa1
    else:
        H += H1; sa += sa1
    continue

import histogram, histogram.hdf as hh
axes = [
    histogram.axis('k', boundaries=edges[0]),
    histogram.axis('E', unit='meV', boundaries=edges[1]),
    ]
h = histogram.histogram('I(k,E)', axes=axes, data=H/sa)
hh.dump(h, 'I_kE.h5')

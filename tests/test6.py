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
        x = 'h', y = 'k', u='l', v='E',
        E=[-1,1], l=[-1,1], 
        h=(-5, 5, 0.02), k=(-5, 5, 0.02),
        )
    return H, edges


H = None; edges = None
for i in range(28880, 29000):
# for i in range(28880, 28920):
    path = os.path.join(dir, "HYS_%d_4pixel.nxspe" % i)
    H1, edges1 = process(path)
    if H is None:
        H, edges = H1, edges1
    else:
        H += H1
    continue

import histogram, histogram.hdf as hh
axes = [
    histogram.axis('h', boundaries=edges[0]),
    histogram.axis('k', boundaries=edges[1]),
    ]
h = histogram.histogram('I(h,k)', axes=axes, data=H)
hh.dump(h, 'I_hk.h5')

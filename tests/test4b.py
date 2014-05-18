#!/usr/bin/env python

import os, numpy as np

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")

def process(path):
    basename,ext = os.path.splitext(os.path.basename(path))
    
    from nslice.Run import Run
    run = Run(path)
    print "instrument=%s, Ei=%s, psi=%s" % (
        run.instrument, run.Ei, run.psi)

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
        E=[-2,2], l=[-5,5], 
        h=(-5, 5, 0.02), k=(-5, 5, 0.02),
        )
    import histogram, histogram.hdf as hh
    axes = [
        histogram.axis('h', boundaries=edges[0]),
        histogram.axis('k', boundaries=edges[1]),
        ]
    h = histogram.histogram('I(h,k)', axes=axes, data=H)
    hh.dump(h, '%s-I_hk.h5' % basename)
    return


i = 28880
path = os.path.join(dir, "HYS_%d_4pixel.nxspe" % i)
process(path)


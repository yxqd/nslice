#!/usr/bin/env python

import os, numpy as np

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")

def process(path):
    basename = os.path.basename(path)
    
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
    
    from nslice.slice import slice_hE
    H, edges = slice_hE(
        hklEIE, 
        k=[0.95,1.05], l=[-1,1], 
        h=(-1, 6, 0.02), E=(-5, 10, 0.1),
        )
    import histogram, histogram.hdf as hh
    axes = [
        histogram.axis('h', boundaries=edges[0]),
        histogram.axis('E', unit='meV', boundaries=edges[1]),
        ]
    h = histogram.histogram('I(h,E)', axes=axes, data=H)
    hh.dump(h, 'I_hE.h5')
    return


i = 28880
path = os.path.join(dir, "HYS_%d_4pixel.nxspe" % i)
process(path)


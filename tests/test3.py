#!/usr/bin/env python

import os

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")

def process(path):
    basename = os.path.basename(path)
    
    from nslice.Run import Run
    run = Run(path)
    print "instrument=%s, Ei=%s, psi=%s" % (
        run.instrument, run.Ei, run.psi)

    from nslice.XtalOrientation import XtalOrientation
    a = b = c = 3
    from math import pi
    twopi = 2*pi
    ra,rb,rc = [twopi/a, 0,0], [0,twopi/b,0], [0,0,twopi/c]
    u,v = [1,0,0], [0,1,0]
    xtal_ori = XtalOrientation(ra,rb,rc, u,v, run.psi)

    hklE = run.compute_hklE(xtal_ori)
    hklE.tofile('%s-hklE.nparr' % basename)
    return


for i in range(28880, 28899):
    path = os.path.join(dir, "HYS_%d_4pixel.nxspe" % i)
    process(path)


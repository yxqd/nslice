#!/usr/bin/env python

import os

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")
path = os.path.join(dir, "HYS_28880_4pixel.nxspe")

from nslice.Run import Run
run = Run(path)
print "instrument=%s, Ei=%s, psi=%s" % (
    run.instrument, run.Ei, run.psi)



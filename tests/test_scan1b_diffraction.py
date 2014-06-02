#!/usr/bin/env python

import os, numpy as np

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")
filename_template = "HYS_%d_4pixel.nxspe"
run_numbers = range(28880, 29084)
from nslice.Scan import Scan
scan = Scan(dir, filename_template, run_numbers)

from nslice.XtalOrientation import XtalOrientation
a = b = 8.87;  c = 5.2
from math import pi
twopi = 2*pi
ra,rb,rc = [twopi/a, 0,0], [0,twopi/b,0], [0,0,twopi/c]
u,v = [1,0,0], [0,1,0]
xtal_ori = XtalOrientation(ra,rb,rc, u,v, 0)

print "computing projections..."
scan.computeProjections(xtal_ori)
print "computing slice..."
h = scan.computeSlice(
    x = 'h', y = 'k', u = 'E', v = 'l',
    E=[-2,2], l=[-5,5], 
    h=(-2, 4, 0.02), k=(-2, 4, 0.02),
    )
import histogram, histogram.hdf as hh
hh.dump(h, 'scan1b-I_hk.h5')

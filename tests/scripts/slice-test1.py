import os, numpy as np

dir = os.path.expanduser("~/simulations/HYSPEC/kvo/exp")
filename_template = "HYS_%d_4pixel.nxspe"
run_numbers = range(28880, 29000)
from nslice.Scan import Scan
scan = Scan(dir, filename_template, run_numbers)

poolsize = 10

slice_opts = dict(
    x = 'k', y = 'E', u = 'h', v = 'l',
    k=(-1,4,.03), E=(0,6,0.1), 
    h=(0.95,1.05), l=(-1,1),
    )

#!/usr/bin/env python

import sys
args_py = sys.argv[1]
code = open(args_py).read()
context = dict()
exec code in context

xtal_ori = context['xtal_ori']
scan = context['scan']
poolsize = context['poolsize']

def one(f):
    scan.computeProjectionsForOneRun(f, xtal_ori)
    return

from multiprocessing import Pool
p = Pool(poolsize)
p.map(one, scan.paths)

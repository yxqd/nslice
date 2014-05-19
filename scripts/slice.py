#!/usr/bin/env python

import sys
args_py = sys.argv[1]
code = open(args_py).read()
context = dict()
exec code in context

scan = context['scan']
poolsize = context['poolsize']
slice_opts = context['slice_opts']

import numpy as np
def one(f, H, sa):
    H = np.frombuffer(H.get_obj())
    sa = np.frombuffer(sa.get_obj())
    edges, H1, sa1 = scan.computeSliceForOneRun(f, **slice_opts)
    H.shape = sa.shape = H1.shape
    H += H1; sa += sa1
    return


def worker(work_q, H, sa):
    while not work_q.empty():
        f = work_q.get()
        print f
        one(f, H, sa)
        continue
    return


def mparr2nparr(a):
    return np.frombuffer(a.get_obj())


def main():
    from nslice.slice import slice_output_dims
    shape, edges = slice_output_dims(None, **slice_opts)
    size = shape[0] * shape[1]
    
    from multiprocessing import Process, Array, Queue
    shared_H = Array('d', size)
    shared_sa = Array('d', size)

    work_q = Queue()
    print scan.paths
    for path in scan.paths: work_q.put(path)
    print work_q

    processes = []
    for w in xrange(poolsize):
        p = Process(target=worker, args=(work_q, shared_H, shared_sa))
        p.start()
        processes.append(p)
        continue

    for p in processes:
        p.join()

    
    import histogram
    axes = [
        histogram.axis(slice_opts['x'], boundaries=edges[0]),
        histogram.axis(slice_opts['y'], boundaries=edges[1]),
        ]
    H = mparr2nparr(shared_H)
    sa = mparr2nparr(shared_sa)
    H.shape = sa.shape = shape
    h = histogram.histogram('I(%(x)s,%(y)s)'%slice_opts, axes=axes, data=H/sa)
    import histogram.hdf as hh
    hh.dump(h, 'new.h5')
    return



if __name__ == '__main__': main()

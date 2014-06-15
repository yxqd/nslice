# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


from .. import name as cliname
from . import name as cmdname
actionname = ''

def run(scan=None, poolsize=None, output=None, **volume_opts):
    scan = load_mod(scan)['scan']
    
    def worker(work_q, H, sa):
        while not work_q.empty():
            f = work_q.get()
            print f
            one(f, H, sa, scan, volume_opts)
            continue
        return

    shape, edges = scan.volumeOutputDims(**volume_opts)
    size = shape[0] * shape[1] * shape[2]
    
    from multiprocessing import Process, Queue, Array
    shared_H = Array('d', size)
    shared_sa = Array('d', size)
    work_q = Queue()
    for path in scan.paths: work_q.put(path)
    
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
        histogram.axis(volume_opts['x'], boundaries=edges[0]),
        histogram.axis(volume_opts['y'], boundaries=edges[1]),
        histogram.axis(volume_opts['z'], boundaries=edges[2]),
        ]
    H = mparr2nparr(shared_H)
    sa = mparr2nparr(shared_sa)
    H.shape = sa.shape = shape
    h = histogram.histogram(
        'I(%(x)s,%(y)s,%(z)s)'%volume_opts, axes=axes, data=H/sa)
    import histogram.hdf as hh
    hh.dump(h, output)
    return


def one(f, H, sa, scan, volume_opts):
    H = np.frombuffer(H.get_obj())
    sa = np.frombuffer(sa.get_obj())
    edges, H1, sa1 = scan.computeVolumeForOneRun(f, **volume_opts)
    H.shape = sa.shape = H1.shape
    H += H1; sa += sa1
    return


def parse_cmdline():
    print ("%s %s %s: make volume\n" % (cliname, cmdname, actionname))
    
    import optparse
    cmd1 =  "%prog " + cmdname + " " + actionname
    usage = "usage: " + cmd1 + " [options]\n"
    usage += "\n * Example:\n"
    usage += "   $ " + cmd1 + ""
    
    parser = optparse.OptionParser(usage, add_help_option=True, option_class=MyOption)
    
    parser.add_option('-s', '--scan', type="str", default="i.scan", dest='scan')
    parser.add_option('-n', '--poolsize', type="int", default=10, dest='poolsize')
    parser.add_option('-o', '--output', type="str", default="out.h5", dest='output')

    parser.add_option('-x', '--x', type="str", default="h", dest='x')
    parser.add_option('-y', '--y', type="str", default="k", dest='y')
    parser.add_option('-z', '--z', type="str", default="E", dest='z')
    parser.add_option('-u', '--u', type="str", default="l", dest='u')
    
    parser.add_option('', '--h', type="axis", default="", dest='h')
    parser.add_option('', '--k', type="axis", default="", dest='k')
    parser.add_option('', '--l', type="axis", default="", dest='l')
    parser.add_option('', '--E', type="axis", default="", dest='E')
    
    #
    options, args = parser.parse_args()
    if len(args) > 2:
        parser.error("too many arguments\n\n")
        
    kwds = vars(options)
    return [], kwds


import numpy as np
from .._utils import mparr2nparr, load_mod, MyOption


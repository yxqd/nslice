# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


from .. import name as cliname
from . import name as cmdname
actionname = ''

import os
def run(xtal_ori=None, scan=None, poolsize=None):
    xtal_ori = load_mod(xtal_ori)['xtal_ori']
    scan = load_mod(scan)['scan']
    
    def work(f_q):
        while not f_q.empty():
            f = f_q.get()
            scan.computeProjectionsForOneRun(f, xtal_ori)
            continue
        return

    from multiprocessing import Process, Queue
    f_q = Queue()
    for path in scan.paths: f_q.put(path)
    
    processes = []
    for w in xrange(poolsize):
        p = Process(target=work, args=(f_q,))
        p.start()
        processes.append(p)
        continue
    for p in processes:
        p.join()
    return


def load_mod(f):
    if not os.path.exists(f):
        raise IOError("%s does not exist" % f)
    code = open(f).read()
    context = dict()
    exec code in context
    return context


def parse_cmdline():
    print ("%s %s %s: make projections\n" % (cliname, cmdname, actionname))
    
    import optparse
    cmd1 =  "%prog " + cmdname + " " + actionname
    usage = "usage: " + cmd1 + " [options]\n"
    usage += "\n * Example:\n"
    usage += "   $ " + cmd1 + ""
    
    parser = optparse.OptionParser(usage, add_help_option=True)
    
    parser.add_option('-x', '--xtal-ori', type="str", default="i.xtal_ori", dest='xtal_ori')
    parser.add_option('-s', '--scan', type="str", default="i.scan", dest='scan')
    parser.add_option('-n', '--poolsize', type="int", default=10, dest='poolsize')
    
    #
    options, args = parser.parse_args()
    if len(args) > 2:
        parser.error("too many arguments\n\n")
        
    kwds = vars(options)
    return [], kwds



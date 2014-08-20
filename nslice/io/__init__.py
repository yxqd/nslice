# -*- python -*-
# Jiao Lin <linjiao@caltech.edu>


load_xtal_ori = lambda f: load_mod(f)['xtal_ori']
load_scan = lambda f: load_mod(f)['scan']


def load_mod(f):
    if not os.path.exists(f):
        raise IOError("%s does not exist" % f)
    code = open(f).read()
    context = dict()
    exec code in context
    return context



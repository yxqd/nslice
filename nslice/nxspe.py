# -*- python -*-

import h5py

def read(path):
    import h5py
    f = h5py.File(path, mode='r')
    try:
        entry = f.values()[0]
    except:
        raise RuntimeError("no entry? %s" % path)
    return f, entry


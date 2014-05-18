# -*- python -*-

import h5py

def read(path):
    import h5py
    f = h5py.File(path)
    entry = f.values()[0]
    return entry


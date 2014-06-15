# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


class Projection:
    
    data = None
    bounds = None



import h5py
class ProjectionFile:
    
    def __init__(self, path):
        self.path = path
        return
    
    
    def write(self, proj):
        f = h5py.File(self.path, 'a')
        f['data'] = proj.data
        f['bounds'] = proj.bounds
        return 
    
    
    def readData(self):
        f = h5py.File(self.path, 'r')
        return f['data'][:]

    
    def readBounds(self):
        f = h5py.File(self.path, 'r')
        return f['bounds'][:]
        
    
    

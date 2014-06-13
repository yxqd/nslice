# -*- python -*-


"""
Run file based on histogram.
"""

from numpy import pi
deg2rad = pi/180


from .AbstractRun import AbstractRun as base
class Run(base):
    
    def __init__(self, path):
        self.path = path
        self.read_metadata()
        return


    def read_metadata(self):
        import h5py
        f = h5py.File(self.path)
        entry = f['I(theta, phi, E)']
        self.Ei = float(entry.attrs['Ei'])
        self.psi = float(entry.attrs['psi']) * deg2rad
        self.instrument = str(entry.attrs['instrument'])
        del entry
        f.close()
        return
    
    
    def read_pixE(self):
        from histogram.hdf import load
        self.histogram = load(self.path)
        phi = self.histogram.phi * deg2rad
        nphi = len(phi)
        theta = self.histogram.theta * deg2rad
        ntheta = len(theta)
        import numpy as np
        phi = np.tile(phi, ntheta)
        theta = np.repeat(theta, nphi)
        energy = self.histogram.E
        return energy, theta, phi
    
    
    def read_data(self):
        I = self.histogram.I
        import numpy as np
        E = np.sqrt(self.histogram.E2)
        return I, E
    
    
    

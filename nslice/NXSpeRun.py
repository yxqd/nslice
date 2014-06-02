# -*- python -*-


from numpy import pi
deg2rad = pi/180


from .AbstractRun import AbstractRun as base
class Run(base):
    
    def __init__(self, path):
        self.path = path
        from .nxspe import read
        self.h5f, self.entry = read(path)
        self.read_metadata()
        return


    def __del__(self):
        del self.entry
        self.h5f.close()
        return
    
    
    def read_metadata(self):
        self.Ei = self.entry['NXSPE_info']['fixed_energy'][0]
        self.psi = self.entry['NXSPE_info']['psi'][0] * deg2rad
        self.instrument = self.entry['instrument']['name'][0]
        return

    
    def read_pixE(self):
        phi = self.entry['data']['azimuthal'][:] * deg2rad
        theta = self.entry['data']['polar'][:] * deg2rad
        # these are boundaries
        energy = self.entry['data']['energy'][:]
        # convert to centers
        energy = (energy[:-1] + energy[1:])/2
        return energy, theta, phi
    
    
    def read_data(self):
        I = self.entry['data']['data'][:]
        E = self.entry['data']['error'][:]
        return I, E
    
    
    

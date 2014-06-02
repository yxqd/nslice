# -*- python -*-


from numpy import pi
deg2rad = pi/180


class AbstractRun:
    
    def read_metadata(self):
        self.Ei = None
        self.psi = None
        self.instrument = None
        return

    
    def read_pixE(self):
        phi = None
        theta = None
        energy = None
        return energy, theta, phi
    
    
    def read_data(self):
        I = None
        E = None
        return I, E
    
    
    def compute_hklE(self, xtal_orientation):
        energy, theta, phi = self.read_pixE()
        Ef = self.Ei - energy
        mat = xtal_orientation.cartesian2hkl_mat()
        from .spe2hkle import spe2hkle
        return spe2hkle(self.Ei, Ef, theta, phi, mat)
    

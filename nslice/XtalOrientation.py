# -*- python -*-


class XtalOrientation:
    
    
    def __init__(self, ra, rb, rc, u, v, psi):
        self.ra = np.array(ra)
        self.rb = np.array(rb)
        self.rc = np.array(rc)
        self.u = np.array(u)
        self.v = np.array(v)
        self.psi = psi
        return
    
    
    def cartesian2hkl_mat(self):
        from .spe2hkle import xtalori2mat
        return xtalori2mat(
            self.ra, self.rb, self.rc, 
            self.u, self.v, self.psi,
            )
    
import numpy as np

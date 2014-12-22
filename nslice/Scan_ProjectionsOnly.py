# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


import os, numpy as np

from .Scan import Scan as base
class Scan_ProjectionsOnly(base):
    
    """A scan that consists of projection files only. 
    no need of nxspe
    """
    
    def __init__(
        self,
        dir, filename_template, run_numbers,
        name=None,
        ):
        self.name = name or ('projs-%s' % os.path.basename(dir))
        self.dir = dir
        self.filename_template = filename_template
        self.run_numbers = run_numbers
        self.paths = [
            os.path.join(dir, filename_template % run_number)
            for run_number in run_numbers
            ]
        return


    def get_projection_filename(self, nxspepath):
        raise RuntimeError
    def get_projection_filepath(self, nxspepath):
        raise RuntimeError
    
    
    def getProjectionBounds(self, paths=None):
        paths = paths or self.paths
        N = len(paths)
        t = np.zeros((N,8), dtype=np.double)
        for i,path in enumerate(paths):
            t[i] = self.getProjectionBoundsForOneRun(path)
            continue
        return np.min(t[:,0]), np.max(t[:,1]), \
            np.min(t[:,2]), np.max(t[:,3]), \
            np.min(t[:,4]), np.max(t[:,5]), \
            np.min(t[:,6]), np.max(t[:,7])
    
    
    def getProjectionBoundsForOneRun(self, path):
        """get the upper and lower bounds of h,k,l,E for a projection file
        """
        from .Projection import ProjectionFile
        pf = ProjectionFile(path)
        return pf.readBounds()
    
    
    def readProjections(self, path):
        from .Projection import ProjectionFile
        pf = ProjectionFile(path)
        return pf.readData()
    
    
    def computeProjectionsForOneRun(self, path, xtal_orientation):
        raise RuntimeError(
            "%s does not support computeProjectionsForOneRun" %
            self.__class__.__name__
            )
    
    
    def computeProjections(self, xtal_orientation):
        raise RuntimeError
    
    

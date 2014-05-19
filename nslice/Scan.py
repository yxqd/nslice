# -*- python -*-


import os, numpy as np

class Scan:
    
    """A scan is a series of runs which only differ by 'psi' angles
    """
    
    def __init__(
        self, dir, filename_template, run_numbers,
        psi_offset=0, name=None,
        ):
        self.name = name or ('scan-%s' % os.path.basename(dir))
        self.dir = dir
        self.filename_template = filename_template
        self.run_numbers = run_numbers
        self.psi_offset = psi_offset
        self.paths = [
            os.path.join(dir, filename_template % run_number)
            for run_number in run_numbers
            ]
        wd = self.workdir()
        if not os.path.exists(wd):
            os.makedirs(wd)
        return


    def workdir(self): return 'work-%s' % self.name
    
    
    projection_filename_template = 'proj-%s.npyarr'
    def get_projection_filename(self, nxspepath):
        basename,ext = os.path.splitext(os.path.basename(nxspepath))
        return self.projection_filename_template % basename
    def get_projection_filepath(self, nxspepath):
        fn = self.get_projection_filename(nxspepath)
        return os.path.join(self.workdir(), fn)
    
    
    def readProjections(self, nxspepath):
        f = self.get_projection_filepath(nxspepath)
        arr = np.fromfile(f)
        arr.shape = 6,-1
        return arr
    
    
    def computeProjectionsForOneRun(self, path, xtal_orientation):
        from .Run import Run
        xo = xtal_orientation
        print path
        ofile = self.get_projection_filepath(path)
        if os.path.exists(ofile):
            print "%s already exists. skip" % ofile
            return
        run = Run(path)
        xo.psi = run.psi + self.psi_offset
        h,k,l,E = run.compute_hklE(xo)
        I, error = run.read_data()
        h.shape = k.shape = l.shape = E.shape = I.shape = error.shape = -1
        hklEIE = np.vstack((h,k,l,E,I,error))
        hklEIE.tofile(ofile)
        return
    
    
    def computeProjections(self, xtal_orientation):
        from .Run import Run
        xo = xtal_orientation
        for path in self.paths:
            self.computeProjectionsForOneRun(path)
            continue
        return
    
    
    def computeSliceForOneRun(self, path, **kwds):
        proj = self.readProjections(path)
        from nslice.slice import slice
        H, edges = slice(proj, **kwds)
        
        h,k,l,E, I, error = proj
        shape = h.shape
        solidangle_I = np.ones(shape, dtype='double')
        solidangle_error = np.zeros(shape, dtype='double')
        hklEIE = np.vstack((h,k,l,E,solidangle_I,solidangle_error))
        sa, edges = slice(hklEIE, **kwds)
        return edges, H, sa
    
    
    def computeSlice(self, paths=None, **kwds):
        H = None; sa = None; edges = None
        for path in paths or self.paths:
            print path
            edges1, H1, sa1 = self.computeSliceForOneRun(path, **kwds)
            if H is None:
                edges, H, sa = edges1, H1, sa1
            else:
                H += H1; sa += sa1
            continue
        
        import histogram
        axes = [
            histogram.axis(kwds['x'], boundaries=edges[0]),
            histogram.axis(kwds['y'], boundaries=edges[1]),
            ]
        return histogram.histogram('I(%(x)s,%(y)s)'%kwds, axes=axes, data=H/sa)

    

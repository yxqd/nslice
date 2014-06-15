# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


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
    
    
    projection_filename_template = 'proj-%s.h5'
    def get_projection_filename(self, nxspepath):
        basename,ext = os.path.splitext(os.path.basename(nxspepath))
        return self.projection_filename_template % basename
    def get_projection_filepath(self, nxspepath):
        fn = self.get_projection_filename(nxspepath)
        return os.path.join(self.workdir(), fn)
    
    
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
    
    
    def getProjectionBoundsForOneRun(self, nxspepath):
        """get the upper and lower bounds of h,k,l,E for a projection file
        """
        f = self.get_projection_filepath(nxspepath)
        from .Projection import ProjectionFile
        pf = ProjectionFile(f)
        return pf.readBounds()
    
    
    def readProjections(self, nxspepath):
        f = self.get_projection_filepath(nxspepath)
        from .Projection import ProjectionFile
        pf = ProjectionFile(f)
        return pf.readData()
    
    
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
        from .Projection import Projection, ProjectionFile
        proj = Projection(); proj.data = hklEIE
        bounds = np.nanmin(h), np.nanmax(h), np.nanmin(k), np.nanmax(k),\
            np.nanmin(l), np.nanmax(l), np.nanmin(E), np.nanmax(E)
        proj.bounds = np.array(bounds)
        pf = ProjectionFile(ofile)
        pf.write(proj)
        return
    
    
    def computeProjections(self, xtal_orientation):
        from .Run import Run
        xo = xtal_orientation
        for path in self.paths:
            self.computeProjectionsForOneRun(path, xtal_orientation)
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

    
    def computeVolumeForOneRun(self, path, **kwds):
        kwds = self._setBounds(kwds)
        proj = self.readProjections(path)
        from nslice.volume import volume
        H, edges = volume(proj, **kwds)
        
        h,k,l,E, I, error = proj
        shape = h.shape
        solidangle_I = np.ones(shape, dtype='double')
        solidangle_error = np.zeros(shape, dtype='double')
        hklEIE = np.vstack((h,k,l,E,solidangle_I,solidangle_error))
        sa, edges = volume(hklEIE, **kwds)
        return edges, H, sa
    
    
    def computeVolume(self, paths=None, **kwds):
        H = None; sa = None; edges = None
        for path in paths or self.paths:
            print path
            edges1, H1, sa1 = self.computeVolumeForOneRun(path, **kwds)
            if H is None:
                edges, H, sa = edges1, H1, sa1
            else:
                H += H1; sa += sa1
            continue
        
        import histogram
        axes = [
            histogram.axis(kwds['x'], boundaries=edges[0]),
            histogram.axis(kwds['y'], boundaries=edges[1]),
            histogram.axis(kwds['z'], boundaries=edges[2]),
            ]
        return histogram.histogram(
            'I(%(x)s,%(y)s,%(z)s)'%kwds, 
            axes=axes, data=H/sa,
            )
    
    
    def volumeOutputDims(self, **kwds):
        kwds = self._setBounds(kwds)
        from .volume import volume_output_dims
        return volume_output_dims(None, **kwds)
    

    def _setBounds(self, opts):
        opts = dict(opts)
        bounds = self.getProjectionBounds()
        hmin, hmax, kmin, kmax, lmin, lmax, Emin, Emax = bounds
        for axis in 'hklE':
            if opts[axis] is not None:
                self._setAxisBounds(axis, opts, locals())
            continue
        return opts
    
    
    def _setAxisBounds(self, axisname, opts, context):
        min, max, step = opts[axisname]
        if min is None: min = context['%smin'%axisname]
        if max is None: max = context['%smax'%axisname]
        opts[axisname] = min, max, step
        return

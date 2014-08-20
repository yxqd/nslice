# -*- python -*-

# ipython --gui=wx
"""
import histogram.hdf as hh
h = hh.load('IhkE2.h5')
"""


from mayavi import mlab


def volume(h, min=None, max=None):
    mlab.pipeline.volume(mlab.pipeline.scalar_field(h.I), vmin=min, vmax=max)
    return

def slice(hist, min=None, max=None, **kwds):
    assert len(kwds.items()) == 1
    axisname = kwds.keys()[0]
    value = kwds.values()[0]
    centers = getattr(hist, axisname)
    axisnames = [a.name() for a in hist.axes()]
    step = centers[1] - centers[0]
    index = int(round((value - centers[1]) / step))
    mlab.pipeline.image_plane_widget(
        mlab.pipeline.scalar_field(hist.I),
        plane_orientation='%s_axes' % ('xyz'[axisnames.index(axisname)],),
        slice_index=index, 
        vmin=min, vmax=max)

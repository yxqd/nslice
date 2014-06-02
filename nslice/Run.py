# -*- python -*-


from numpy import pi
deg2rad = pi/180


def Run(path):
    import os
    base, ext = os.path.splitext(path)
    factory = factories[ext]
    return factory(path)


from .NXSpeRun import Run as NXSpeRun
factories = {
    '.nxspe': NXSpeRun,
    }

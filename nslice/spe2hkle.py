# -*- python -*-


import numpy as np

def spe2hkle(Ei, Ef, theta, phi, mat):
    """convert spe data to hklE data
    
    Ei: float
    Ef: array
    theta: array
    phi: array
    mat: matrice (can be obtained from xtalori2mat
    x along beam, z vertical
    """
    from .neutron.conversion import V2K, SE2V
    se2k = SE2V * V2K
    kf = np.sqrt(Ef) * se2k   # array of nEf
    # dims
    nEf = kf.size
    npix = theta[:].size
    # each component has shape: npix, nEf
    kfx = np.cos(theta)[:, np.newaxis] * kf[np.newaxis, :]
    kfy = (np.sin(theta) * np.cos(phi))[:, np.newaxis] * kf[np.newaxis, :]
    kfz = (np.sin(theta) * np.sin(phi))[:, np.newaxis] * kf[np.newaxis, :]
    # kf vector
    kfx.shape = kfy.shape = kfz.shape = -1,
    kfv = np.vstack((kfx, kfy, kfz)).T
    # ki vector
    ki = np.sqrt(Ei) * se2k
    kiv = np.array((ki, 0, 0))
    # Q vector
    Qv = kiv - kfv
    # hkl
    h,k,l = np.dot(Qv, mat).T
    h.shape = k.shape = l.shape = npix, nEf
    # E
    E = Ei - Ef
    E = np.tile(E, (npix, 1)); 
    return h,k,l,E



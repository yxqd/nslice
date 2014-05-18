# -*- python -*-


import numpy as np


def xtalori2mat(ra, rb, rc, u, v, psi):
    """create transformation matrices from orientation spec
    inputs: reciprocal laticce vectors, u/v vectors, and psi angle
    """
    # rotate u, v by psi angle
    from math import cos, sin
    u1 = u * cos(psi) - v * sin(psi)
    v1 = u * sin(psi) + v * cos(psi)
    # ra, rb, rc are defined in a orthogonal 
    # coordinate system attached to the crystal
    r = np.array([ra, rb, rc])
    # xyz are unit vectors of the laboratory coordinate system
    # expressed in terms of the crystal coordinate system
    x = np.dot(u1, r); lx=np.linalg.norm(x); x/=lx; u1/=lx
    y = np.dot(v1, r); ly=np.linalg.norm(y); y/=ly; v1/=ly
    z = np.cross(x,y) 
    # now express z with ra, rb, rc
    w = np.dot(np.linalg.inv(r.T), z)
    return np.array([u1,v1,w])


def spe2hkle(Ei, Ef, theta, phi, mat):
    """convert spe data to hklE data
    
    Ei: float
    Ef: array
    theta: array
    phi: array
    mat: matrice (can be obtained from xtalori2mat
    """
    from .neutron import V2K, SE2V
    se2k = SE2V * V2K
    kf = np.sqrt(Ef) * se2k   # array of nEf
    # dims
    nEf = kf.size
    npix = theta[:].size
    # each component has shape: npix, nEf
    kfx = np.cos(theta)[:, np.newaxis] * kf[np.newaxis, :]
    kfy = (np.sin(theta) * np.cos(phi))[:, np.newaxis] * kf[np.newaxis, :]
    kfz = (-np.sin(theta) * np.sin(phi))[:, np.newaxis] * kf[np.newaxis, :]
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


def test_xtalori2mat():
    # cubic
    ra, rb, rc = np.array([[1,0,0], [0,1,0], [0,0,1]])
    u,v = np.array([[1,0,0], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        (ra,rb,rc))
    
    psi = np.pi/2
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        (-rb, ra, rc))

    # box
    ra, rb, rc = np.array([[1,0,0], [0,2,0], [0,0,3]])
    u,v = np.array([[1,0,0], [0,0.5,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([1,0,0],[0,0.5,0],[0,0,1./3]))
    
    u,v = np.array([[0,0,1], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([0,0,1./3],[0,0.5,0],[-1,0,0]))
    
    # 
    ra, rb, rc = np.array([[1,0,0], [0,1,0], [1,1,1]])
    u,v = np.array([[1,0,0], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([1,0,0],[0,1,0],[-1,-1,1]))
    
    return


def main():
    test_xtalori2mat()
    return


if __name__ == '__main__': main()

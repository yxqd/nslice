# -*- python -*-


import numpy as np


def xtalori2mat(ra, rb, rc, u, v, psi):
    """create transformation matrices from orientation spec
    inputs: reciprocal laticce vectors, u/v vectors, and psi angle
    
    u/v vectors are vectors in the rotation plane of the crystal
    represented in hkl notation.
    
    The main goal here is to compute three unit vectors
    represented in hkl notation: x, y, z.
    Here z is vertical, x along beam.
    
    u/v vectors are in the x-y plane.
    if psi is 0, u should be x, and v should y.
    """
    # ra, rb, rc are defined in a cartesian
    # coordinate system attached to the crystal (CCSC)
    r = np.array([ra, rb, rc])
    # compute u, v in cartesian coordinate system
    u_cart = np.dot(u, r)
    v_cart = np.dot(v, r)
    # normalize them
    lu = np.linalg.norm(u_cart); u_cart/=lu
    lv = np.linalg.norm(v_cart); v_cart/=lv
    # rotate u, v by psi angle to obtain x,y unit vectors
    from math import cos, sin
    ex = u_cart * cos(psi) - v_cart * sin(psi)
    ey = u_cart * sin(psi) + v_cart * cos(psi)
    # now compute z unit vector in CCSC
    ez = np.cross(ex,ey) 
    # now express xyz with ra, rb, rc, to get hkl
    # dot(r.T, hkl) = cartesian, therefore, dot(r.T**-1, cartesian) = hkl
    invR = np.linalg.inv(r.T)
    x1 = np.dot(invR, ex)
    y1 = np.dot(invR, ey)
    z1 = np.dot(invR, ez)
    return np.array([x1, y1, z1])


def spe2hkle(Ei, Ef, theta, phi, mat):
    """convert spe data to hklE data
    
    Ei: float
    Ef: array
    theta: array
    phi: array
    mat: matrice (can be obtained from xtalori2mat
    x along beam, z vertical
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

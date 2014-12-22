# -*- python -*-


import numpy as np


def xtalori2mat(ra, rb, rc, u, v, psi):
    """create transformation matrices from orientation spec
    inputs: reciprocal laticce vectors, u/v vectors, and psi angle
    output: matrix M that satisfy hkl = Q dot M, where hkl and Q are all row vectors
    
    ra, rb, rc are reciprocal base vectors represented in a cartesian
    coordinate system attached to the crystal.
    
    u/v vectors are vectors in the rotation plane of the crystal
    represented in hkl notation.
    
    The main goal here is to compute three unit vectors
    represented in hkl notation: x, y, z.
    Here z is vertical, x along beam.
    
    u/v vectors are in the x-y plane.
    if psi is 0, u should be x, and v must be in x-y plane.
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
    # u and v is not necesarily perpendicular to each other
    # let us compute z first
    ez = np.cross(u_cart, v_cart); ez/=np.linalg.norm(ez)
    # now we can compute vprime, a unit vector perpedicular to
    # u_cart and ez
    vprime_cart = np.cross(ez, u_cart)
    # rotate u, v by psi angle to obtain x,y unit vectors
    from math import cos, sin
    ex = u_cart * cos(psi) - vprime_cart * sin(psi)
    ey = u_cart * sin(psi) + vprime_cart * cos(psi)
    # now express xyz with ra, rb, rc, to get hkl
    # dot(r.T, hkl) = cartesian, therefore, dot(r.T**-1, cartesian) = hkl
    invR = np.linalg.inv(r.T)
    x1 = np.dot(invR, ex)
    y1 = np.dot(invR, ey)
    z1 = np.dot(invR, ez)
    return np.array([x1, y1, z1])


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

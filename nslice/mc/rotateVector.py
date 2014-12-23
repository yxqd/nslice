# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

# copied from sampleassembly.geometers.rotateVector

from numpy import array,zeros,cos,sin, dot, transpose              
import numpy                                                                  


def toMatrix( *args, **kwds ):
    '''convert rotation angles to a rotation matrix.
the rotation matrix is related to
rotation angles phx, phy, phz as
    
  1. rotate around x axis by angle phx
  2. rotate around y axis by angle phy
  3. rotate around z axis by angle phz

Pleaset note the axis is NOT changed by the rotations!
Sometimes the rotations are described by consecutive rotations
about axes that are rotated by previous rotations.
It is NOT the case here.
Here the axes x, y, z are FIXED in the space!
    
Please be very careful and read the following texts to
understand the meaning of the matrix returned by this function.

The rotation matrix here transforms the vector
to be rotated. Suppose that we have a vector

  v = (x,y,z)

Now we apply rotations to this vector. This vector
will have a new coordinates:

  v1 = (x1, y1, z1)

The matrix that connects v to v1 is the matrix returned
from this function:

  v1 = m . v
    '''
    usage = """toMatrix( 5, 6, 7, unit="deg")
    toMatrix( 5, 6, 7)
    toMatrix( (5,6,7), unit = "deg")
    toMatrix( (5, 6, 7) )
    """
    #if input is already a matrix, just return it
    if len(args) == 1 and isMatrix3(args[0]): return args[0]
    #otherwise we check if the input can be transformed to rotation angles
    if len(args) == 3: #phx, phy, phz
        angles = args
    elif len(args) == 1 and len(args[0]) == 3: # a tuple or list
        angles = args[0]
    else:
        raise SyntaxError, "Usage: %s" % usage
    return _toMatrix( angles[0], angles[1], angles[2], **kwds)
        

def _toMatrix(phx,phy,phz, unit='degree'):
    '''convert rotation angles to a rotation matrix.
    the rotation matrix is related to
    rotation angles phx, phy, phz as
    
    1. rotate around x axis by angle phx
    2. rotate around y axis by angle phy
    3. rotate around z axis by angle phz
    '''
    if unit.lower()=='degree' or unit.lower()=='deg':
        phx = toradian( phx )
        phy = toradian( phy )
        phz = toradian( phz )
    cx = cos(phx);
    sx = sin(phx);
    cy = cos(phy);
    sy = sin(phy);
    cz = cos(phz);
    sz = sin(phz);
    t=zeros((3,3), float )
    t[0][0] = cy*cz;
    t[0][1] = sx*sy*cz - cx*sz;
    t[0][2] = sx*sz + cx*sy*cz;
    t[1][0] = cy*sz;
    t[1][1] = cx*cz + sx*sy*sz;
    t[1][2] = -sx*cz + cx*sy*sz;
    t[2][0] = -sy;
    t[2][1] = sx*cy;
    t[2][2] = cx*cy;
    return t

    
def toAngles(m, unit='degree'):
    '''convert a rotation matrix to angles. the rotation matrix is related to
    rotation angles phx, phy, phz as
    
    1. rotate around x axis by angle phx
    2. rotate around y axis by angle phy
    3. rotate around z axis by angle phz
    
    the conversion here follow similar treatment as those in
    http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToEuler/index.htm
    '''
    #if m is already a tuple of three rotation angles, just return it
    if isVector3(m): return m
    #otherwise we want to make sure m is a Matrix
    if not isMatrix3(m): raise TypeError , "Not a 3X3 matrix: %s" % m
    from numpy import arctan2, arcsin
    if m[2][0]>1-1e-8 :
        #phiy is almost pi*3/2
        x=0. 
        z=arctan2(-m[0][1],m[1][1])
    elif m[2][0]<1e-8-1 :
        #phiy is almost pi/2
        x=0.
        z=arctan2(-m[0][1],m[1][1])
    else :
        z=arctan2(m[1][0],m[0][0])
        x=arctan2(m[2][1],m[2][2])
    y=arcsin(-m[2][0])
    m1=toMatrix(x,y,z, unit='radian')
    try:
        for i in range(3):
            for j in range(3):
                if abs(m[i][j])<1e-8 :
                    if abs(m1[i][j]-m[i][j])>1e-8 :
                        raise 'conversion failed %s' % m
                else :
                    if abs( (m1[i][j]-m[i][j])/m[i][j] )>1e-8 :
                        raise 'conversion failed %s' % m
    except:
        print 'original matrix:',m
        print 'converted matrix:',m1
        raise 'conversion failed %s' % m
    if unit.lower() == 'deg' or unit.lower() == 'degree':
        return map(todegree, (x,y,z))
    else:
        return x,y,z



def test():
    m = toMatrix( 90, 0, 0, unit = 'deg' )
    x,y,z = toAngles( m, unit='deg')
    assert abs(x-90)<1e-8 and abs(y)<1e-8 and abs(z)<1e-8
    
    m = toMatrix( 33, 55, 66, unit = 'deg' )
    x,y,z = toAngles( m, unit='deg')
    assert abs(x-33)<1e-8 and abs(y-55)<1e-8 and abs(z-66)<1e-8
    return


def main():
    test()
    return


if __name__ == '__main__' : main()


# from utils import *
# copied from sampleassembly.geometers.utils
def isMatrix3(m):
    try: tmp = m[0][0]
    except: return False
    if len(m) != 3 or len(m[0]) != 3: return False
    #should we test if every element is a number?
    return True


def isVector3(v):
    try: l = len(v)
    except: return False
    if l!=3 : return False
    for i in v:
        if not isNumber(i): return False
        continue
    return True


def isNumber(i):
    return isinstance(i,int) or isinstance(i,float)
        

def toradian( angle_in_degree ):
    from numpy import pi
    return angle_in_degree*pi/180;

                                                                                
def todegree( angle_in_radian ):
    from numpy import pi
    return angle_in_radian*180/pi;



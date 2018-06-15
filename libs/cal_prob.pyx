import sys
from PIL import Image
#from math import pi,sin,cos,tan,atan2,hypot,floor,radians,sqrt
import numpy as np
cdef float pi=3.14159265358979323846
cdef float R=1920.0/pi
cdef float unit=2*pi/3840.0
cimport numpy as np
cimport cython

cdef extern from "math.h":  
    float cosf(float theta)  
    float sinf(float theta)  
    float acosf(float theta)
    double sqrt(double x)
    double atan2(double y, double x)
    double hypot(double p, double b)
    double floor(double x)

cdef float radians(float x):
    return x*pi/180.0

cdef struct Pos3d:
    float x
    float y
    float z

# get x,y,z coords from out image pixels coords
# i,j are pixel coords
cdef Pos3d outImgToXYZ(int i,int j,float tx,float ty,float tz,float a1,float b1,float c1,float a2,float b2,float c2, float fov_degreew, float fov_degreeh, float fov_sizew, float fov_sizeh):
    cdef Pos3d sp
    cdef float ni = (float(i)-(fov_sizew/2))
    cdef float nj = (float(j)-(fov_sizeh/2))
    if ni==0 and nj==0:
        sp.x=tx
        sp.y=ty
        sp.z=tz
        return sp
    cdef float x = tx+ni*a1+nj*a2
    cdef float y = ty+ni*b1+nj*b2
    cdef float z = tz+ni*c1+nj*c2
    # horizontal and vertical vector from tx,ty,tz
    cdef float vxh=ni*a1
    cdef float vyh=ni*b1
    cdef float vzh=ni*c1
    cdef float vxv=nj*a2
    cdef float vyv=nj*b2
    cdef float vzv=nj*c2
    # unit vector for rotation
    cdef float uxh=ty*vzh-tz*vyh
    cdef float uyh=-tx*vzh+tz*vxh
    cdef float uzh=tx*vyh-ty*vxh
    cdef float uxv=ty*vzv-tz*vyv
    cdef float uyv=-tx*vzv+tz*vxv
    cdef float uzv=tx*vyv-ty*vxv

    if x==tx and y==ty and z==tz:
        sp.x=x
        sp.y=y
        sp.z=z
        return sp
    cdef float normh=sqrt(uxh*uxh+uyh*uyh+uzh*uzh)
    if normh!=0:
        uxh=uxh/normh
        uyh=uyh/normh
        uzh=uzh/normh
    cdef float normv=sqrt(uxv*uxv+uyv*uyv+uzv*uzv)
    if normv!=0:
        uxv=uxv/normv
        uyv=uyv/normv
        uzv=uzv/normv
    if ni<0:
        ni=0-ni
    if nj<0:
        nj=0-nj
    
    cdef float wh=cosf(unit/2*ni)
    cdef float sh=sinf(unit/2*ni)
    cdef float rotxh=sh*uxh
    cdef float rotyh=sh*uyh
    cdef float rotzh=sh*uzh

    cdef float wv=cosf(unit/2*ni)
    cdef float sv=sinf(unit/2*nj)
    cdef float rotxv=sv*uxv
    cdef float rotyv=sv*uyv
    cdef float rotzv=sv*uzv

    cdef np.ndarray uh=np.array([[1.0-2.0*rotyh*rotyh-2.0*rotzh*rotzh, 2.0*rotxh*rotyh-2.0*rotzh*wh, 2.0*rotxh*rotzh+2.0*rotyh*wh],
                   [2.0*rotxh*rotyh+2.0*rotzh*wh, 1.0-2.0*rotxh*rotxh-2.0*rotzh*rotzh, 2.0*rotyh*rotzh-2.0*rotxh*wh],
                   [2.0*rotxh*rotzh-2.0*rotyh*wh, 2.0*rotyh*rotzh+2.0*rotxh*wh, 1.0-2.0*rotxh*rotxh-2.0*rotyh*rotyh]])
    cdef np.ndarray uv=np.array([[1.0-2.0*rotyv*rotyv-2.0*rotzv*rotzv, 2.0*rotxv*rotyv-2.0*rotzv*wv, 2.0*rotxv*rotzv+2.0*rotyv*wv],
                   [2.0*rotxv*rotyv+2.0*rotzv*wv, 1.0-2.0*rotxv*rotxv-2.0*rotzv*rotzv, 2.0*rotyv*rotzv-2.0*rotxv*wv],
                   [2.0*rotxv*rotzv-2.0*rotyv*wv, 2.0*rotyv*rotzv+2.0*rotxv*wv, 1.0-2.0*rotxv*rotxv-2.0*rotyv*rotyv]])
    cdef np.ndarray spt=np.array([[tx],[ty],[tz]],dtype=float)
    spt=uv.dot(spt)
    spt=uh.dot(spt)
    sp.x=spt[0]
    sp.y=spt[1]
    sp.z=spt[2]
    return sp

# convert using an inverse transformation
# def convertBack(imgIn,imgOut,fov_size,fov_degree,ctheta,cphi):
def cal_fovs(ctheta, cphi, float fov_degreew, float fov_degreeh, float tile_w, float tile_h, float fov_sizew, float fov_sizeh):
    probs=[0.0 for i in range(int(tile_w*tile_h))]
    cdef float theta, phi, tx, ty, tz, r
    cdef float a, b, c, d, a1, b1, c1, a2, b2, c2
    cdef norm1, norm2
    cdef float d_square
    cdef Pos3d sp_pos
    cdef float uf, vf, ui, vi, u2, v2, mu, mv
    cdef tile_sizeh, tile_sizew
    tile_sizeh=int(1920.0/float(tile_h))
    tile_sizew=int(3840.0/float(tile_w))
    theta=ctheta
    phi=cphi
    #print ctheta, cphi
    tx=R*sinf(radians(phi))*cosf(radians(theta))
    ty=R*sinf(radians(phi))*sinf(radians(theta))
    tz=R*cosf(radians(phi))
    #print tx,ty,tz
    a = tx
    b = ty
    c = tz
    d = -(tx*tx+ty*ty+tz*tz)
    if theta==0 and (phi==0 or phi==180):
        a1=-1
        b1=0
        c1=0
        a2=0
        b2=-1
        c2=0
    else:
        a1 = b
        b1 = -a
        c1 = 0
        a2 = a*c
        b2 = b*c
        c2 = -a*a-b*b

    norm1=sqrt(a1*a1+b1*b1+c1*c1)
    norm2=sqrt(a2*a2+b2*b2+c2*c2)
    a1=a1/norm1
    b1=b1/norm1
    c1=c1/norm1
    a2=a2/norm2
    b2=b2/norm2
    c2=c2/norm2
    
    for i in xrange(0, int(fov_sizew)):
        for j in xrange(0, int(fov_sizeh)):
            # check whether it is in the circle
            d_square=((i-(fov_sizew/2))*(i-(fov_sizew/2)))/(fov_sizew*fov_sizew/4)+((j-(fov_sizeh/2))*(j-(fov_sizeh/2)))/(fov_sizeh*fov_sizeh/4)
            if d_square>1:
                continue
            sp_pos=outImgToXYZ(fov_sizew-i-1,j,tx,ty,tz,a1,b1,c1,a2,b2,c2,fov_degreew,fov_degreeh,fov_sizew,fov_sizeh)
            theta = atan2(sp_pos.y,sp_pos.x) # range -pi to pi
            r=hypot(sp_pos.x,sp_pos.y)
            phi=atan2(sp_pos.z,r) # range -pi/2 to pi/2
            # source img coords
            uf = int(1920.0*(theta+pi)/pi)%3840
            vf = int(1920.0*(pi/2-phi)/pi)%1920
            # print(uf, vf)
            tile=floor(float(vf)/float(tile_sizeh))*tile_w+floor(float(uf)/float(tile_sizew))
            probs[int(tile)]=1
    return probs

def gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    cdef float fov_sizew = int(float(fov_degreew)/360.0*3840.0)
    cdef float fov_sizeh = int(float(fov_degreeh)/360.0*3840.0)
    if yaw<0:
        yaw=360+yaw
    pitch=90-pitch
    probs=cal_fovs(yaw,pitch,fov_degreew,fov_degreeh,float(tile_w),float(tile_h),fov_sizew,fov_sizeh)
    return probs
    
# convert using an inverse transformation
# def convertBack(imgIn,imgOut,fov_size,fov_degree,ctheta,cphi):
def render_fovs(ctheta, cphi, float fov_degreew, float fov_degreeh, float tile_w, float tile_h, float fov_sizew, float fov_sizeh):
    probs=[0.0 for i in range(int(tile_w*tile_h))]
    cdef float theta, phi, tx, ty, tz, r
    cdef float a, b, c, d, a1, b1, c1, a2, b2, c2
    cdef norm1, norm2
    cdef float d_square
    cdef Pos3d sp_pos
    cdef float uf, vf, ui, vi, u2, v2, mu, mv
    cdef tile_sizeh, tile_sizew
    tile_sizeh=int(1920.0/float(tile_h))
    tile_sizew=int(3840.0/float(tile_w))
    theta=ctheta
    phi=cphi
    #print ctheta, cphi
    tx=R*sinf(radians(phi))*cosf(radians(theta))
    ty=R*sinf(radians(phi))*sinf(radians(theta))
    tz=R*cosf(radians(phi))
    #print tx,ty,tz
    a = tx
    b = ty
    c = tz
    d = -(tx*tx+ty*ty+tz*tz)
    if theta==0 and (phi==0 or phi==180):
        a1=-1
        b1=0
        c1=0
        a2=0
        b2=-1
        c2=0
    else:
        a1 = b
        b1 = -a
        c1 = 0
        a2 = a*c
        b2 = b*c
        c2 = -a*a-b*b

    norm1=sqrt(a1*a1+b1*b1+c1*c1)
    norm2=sqrt(a2*a2+b2*b2+c2*c2)
    a1=a1/norm1
    b1=b1/norm1
    c1=c1/norm1
    a2=a2/norm2
    b2=b2/norm2
    c2=c2/norm2
    
    fixation = []
    for i in xrange(0, int(fov_sizew)):
        for j in xrange(0, int(fov_sizeh)):
            # check whether it is in the circle
            d_square=((i-(fov_sizew/2))*(i-(fov_sizew/2)))/(fov_sizew*fov_sizew/4)+((j-(fov_sizeh/2))*(j-(fov_sizeh/2)))/(fov_sizeh*fov_sizeh/4)
            if d_square>1:
                continue
            sp_pos=outImgToXYZ(fov_sizew-i-1,j,tx,ty,tz,a1,b1,c1,a2,b2,c2,fov_degreew,fov_degreeh,fov_sizew,fov_sizeh)
            theta = atan2(sp_pos.y,sp_pos.x) # range -pi to pi
            r=hypot(sp_pos.x,sp_pos.y)
            phi=atan2(sp_pos.z,r) # range -pi/2 to pi/2
            # source img coords
            uf = int(1920.0*(theta+pi)/pi)%3840
            vf = int(1920.0*(pi/2-phi)/pi)%1920
            fixation.append( (uf, vf) )
            tile=floor(float(vf)/float(tile_sizeh))*tile_w+floor(float(uf)/float(tile_sizew))
            probs[int(tile)]=1
    return (fixation, probs)

def gen_fov(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    cdef float fov_sizew = int(float(fov_degreew)/360.0*3840.0)
    cdef float fov_sizeh = int(float(fov_degreeh)/360.0*3840.0)
    if yaw<0:
        yaw=360+yaw
    pitch=90-pitch
    return render_fovs(yaw,pitch,fov_degreew,fov_degreeh,float(tile_w),float(tile_h),fov_sizew,fov_sizeh)

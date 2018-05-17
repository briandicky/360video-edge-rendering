import numpy
import math
from PIL import Image

PIXEL_MAX = 255.0

NUM_POINTS = 655362

def SPsnrNnCalc(img1, img2):
    width, height = img1.size
    img1_list = list(img1.getdata())
    img2_list = list(img2.getdata())
    img1_list = [img1_list[i * width:(i + 1) * width] for i in range(height)]
    img2_list = [img2_list[i * width:(i + 1) * width] for i in range(height)]
    #Load 655362 sample points
    with open("sphere_655362.txt") as f:
        content = f.readlines()
    sample_points = [x.strip().split() for x in content]
    sample_points.pop(0)
    sample_points = [[float(x[0])*math.pi/180.0, float(x[1])*math.pi/180.0] for x in sample_points]
    #Convert spherical coordinate into Cartesian 3D coordinate
    cart_coord = [[math.sin(x[1])*math.cos(x[0]), math.sin(x[0]), -math.cos(x[1])*math.cos(x[0])] for x in sample_points]
    #Convert Cartesian 3D coordinate into rectangle coordinate
    #phi = math.acos(Y), theta = math.atan2(X, Z)     
    rect_coord = [[width*(0.5 + math.atan2(x[0], x[2])/(math.pi*2)), height*(math.acos(x[1])/math.pi)] for x in cart_coord] 
    #Calculate S_PSNR_NN
    mse = 0
    for pt in rect_coord:
        for ch in range(3):
            pt[0], pt[1] = int(round(pt[0])), int(round(pt[1])) #Nearest Neighbor
            pt[0] = width-1 if pt[0]>=width else pt[0]   #Longtidue
            pt[1] = height-1 if pt[1]>=height else pt[1] #Latitude
            mse += (img1_list[pt[1]][pt[0]][ch] - img2_list[pt[1]][pt[0]][ch])**2
    mse = (mse/(width*height))/3
    if mse == 0:
        return 100
    psnr_value = 10*numpy.log10((PIXEL_MAX**2 /mse))
    return psnr_value

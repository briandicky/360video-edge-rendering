
import numpy
import math

PIXEL_MAX = 255.0

def VPsnrCalc(img1, img2, view):
    height, width, channel = img1.shape
    mse = 0.0
    for pixel in view:
        for k in range(channel):
            mse += (int(img1[int(pixel[1])][int(pixel[0])][k]) - int(img2[int(pixel[1])][int(pixel[0])][k]))**2
    mse = (mse/len(view))/channel
    if mse == 0:
        return 100
    psnr_value = 10*numpy.log10((PIXEL_MAX**2 /mse))
    return psnr_value

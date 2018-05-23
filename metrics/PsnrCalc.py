import numpy
import math

PIXEL_MAX = 255.0

def PsnrCalc(img1, img2):
    height, width, channel = img1.shape
    mse = 0.0
    for i in range(height):
        for j in range(width):
            for k in range(channel):
                mse += (int(img1[i][j][k]) - int(img2[i][j][k]))**2
    mse = (mse/(width*height))/channel
    if mse == 0:
        return 100
    psnr_value = 10*numpy.log10((PIXEL_MAX**2 /mse))
    return psnr_value

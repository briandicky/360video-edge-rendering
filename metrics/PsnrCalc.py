import numpy
import math
from PIL import Image

PIXEL_MAX = 255.0

def PsnrCalc(img1, img2):
    width, height = img1.size
    img1_list = list(img1.getdata())
    img2_list = list(img2.getdata())
    img1_list = [img1_list[i * width:(i + 1) * width] for i in range(height)]
    img2_list = [img2_list[i * width:(i + 1) * width] for i in range(height)]
    mse = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):
                mse += (img1_list[i][j][k] - img2_list[i][j][k])**2
    mse = (mse/(width*height))/3
    #mse = numpy.mean( (img1_list - img2_list)** 2)
    if mse == 0:
        return 100
    psnr_value = 10*numpy.log10((PIXEL_MAX**2 /mse))
    return psnr_value

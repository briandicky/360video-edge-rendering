
import numpy
import math

PIXEL_MAX = 255.0

def PsnrTiledCalc(img1, img2,view_list, mode = 5):
    height, width, channel = img1.shape
    mse = 0.0
    tiled_h = height/5
    tiled_w = width/5
    for t in view_list:
	y1 = (t-2)/5 * tiled_h
	x1 = (t-2)%5 * tiled_w
        for i in range(y1, y1+tiled_h):
            for j in range( x1, x1+tiled_w):
                for k in range(channel):
                    mse += (int(img1[i][j][k]) - int(img2[i][j][k]))**2
    mse = (mse/(tiled_h * tiled_w * len(view_list)))/channel
    if mse == 0:
        return 100
    psnr_value = 10*numpy.log10((PIXEL_MAX**2 /mse))
    return psnr_value

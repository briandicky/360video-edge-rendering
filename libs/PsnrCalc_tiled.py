
import numpy
import math

PIXEL_MAX = 255.0

def PsnrTiledCalc(img1, img2, view_list):
    height, width, channel = img1.shape
    mse = 0.0
    tiled_h = height/5
    tiled_w = width/5
    for t in view_list:
	y1 = (t-2)/5 * tiled_h
	x1 = (t-2)%5 * tiled_w
        for i in range(y1, y1+tiled_h):
            for j in range(x1, x1+tiled_w):
                # video or image will be stored in the BGR format
                # Y = 0.299*R + 0.587*G + 0.114*B
                Y_rec = 0.299*img1[i][j][2] + 0.587*img1[i][j][1] + 0.114*img1[i][j][0]
                Y_ori = 0.299*img2[i][j][2] + 0.587*img2[i][j][1] + 0.114*img2[i][j][0]
                mse += (Y_ori - Y_rec)**2

    mse = mse/(tiled_h * tiled_w * len(view_list))

    if mse == 0:
        return 100

    psnr_value = 10*numpy.log10((PIXEL_MAX**2 / mse))
    return psnr_value


import numpy
import math

PIXEL_MAX = 255.0

def VPsnrCalc(img1, img2, view):
    height, width, channel = img1.shape
    mse = 0.0

    for pixel in view:
        # video or image will be stored in the BGR format
        # Y = 0.299*R + 0.587*G + 0.114*B
        Y_rec = 0.299*img1[int(pixel[1])][int(pixel[0])][2] + 0.587*img1[int(pixel[1])][int(pixel[0])][1] + 0.114*img1[int(pixel[1])][int(pixel[0])][0] 
        Y_ori = 0.299*img2[int(pixel[1])][int(pixel[0])][2] + 0.587*img2[int(pixel[1])][int(pixel[0])][1] + 0.114*img2[int(pixel[1])][int(pixel[0])][0] 
        mse += (Y_ori - Y_rec)**2

    mse = mse/len(view)

    if mse == 0:
        return 100

    psnr_value = 10*numpy.log10((PIXEL_MAX**2 / mse))
    return psnr_value

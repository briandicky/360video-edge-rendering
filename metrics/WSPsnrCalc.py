import numpy
import math

PIXEL_MAX = 255.0
#Input should be ndarrays
def WSPsnrCalc(img1, img2):
    height, width, channel = img1.shape
    weight_list = [[math.cos((i+0.5-height/2)*math.pi/height) for j in range(width)] for i in range(height)]
    weight_sum = 0.0
    wmse = 0.0
    for i in range(height):
        for j in range(width):
			weight_sum += weight_list[i][j]
    for i in range(height):
        for j in range(width):
			for k in range(channel):
	   			wmse += ((int(img1[i][j][k]) - int(img2[i][j][k]))**2)*weight_list[i][j]/channel
    wmse = (wmse/(width*height))/channel
    if wmse == 0:
        return 100
    ws_psnr = 10*numpy.log10((PIXEL_MAX**2 /wmse))
    return ws_psnr

import numpy
import math
from PIL import Image

PIXEL_MAX = 255.0
#Input should be ndarrays
def WSPsnrCalc(img1, img2):
    height, width, channel = img1.shape
    print("aaa")
    weight_list = [[math.cos((i+0.5-height/2)*math.pi/height) for j in range(width)] for i in range(height)]
    print("ccc")
    weight_sum = 0.0
    wmse = 0.0
    for i in range(height):
	print(i)
        for j in range(width):
            for k in range(channel):#RGB
		if(weight_list[i][j] < 0):
		    print("fuck!!!")
		    return 99999
	        wmse += ((img1[i][j][k] - img2[i][j][k])**2)*weight_list[i][j]/channel
	    weight_sum += weight_list[i][j]
    wmse = (wmse/(width*height))/channel
    print("MSE:")
    print(wmse)
    if wmse == 0:
        return 100
    ws_psnr = 10*numpy.log10((PIXEL_MAX**2 /wmse))
    return ws_psnr

import os
import cv2
import math
from PIL import Image

YAW     = -120.03605833333
PITCH   = 0.103563888889
ROLL    = -3.993

WIDTH   = 3840
HEIGHT  = 1920

RADIUS  = WIDTH / (2 * math.pi)

def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def get_pixel(image, i, j):
    # inside image bounds or not 
    width, height = image.size
    if i > width or j > height:
        return None
    # get pixel 
    pixel = image.getpixel( (i, j) )
    return pixel

def video_2_image(path):
    create_path('./frame/')
    vidcap = cv2.VideoCapture(path)
    success, frame = vidcap.read()
    count = 1
    success = True

    while success:
        # save frame as PNG format
        cv2.imwrite("./frame/frame%d.png" % count, frame)
        success, frame = vidcap.read()
        print "Read a new frame: %s", count
        count += 1 

def ori_2_fixation(yaw, pitch):
    # yaw boundary correction
    if yaw > 180:
        yaw = yaw % (-180)
    elif yaw < (-180):
        yaw = yaw % 180
    else:
        print("Should not be here.")

    # pitch boundary correction
    if pitch > 90:
        pitch = pitch - 90
        if yaw > 0:
            yaw = yaw - 180
        else:
            yaw = yaw + 180
    elif pitch < (-90):
        pitch = (-180) - pitch
        if yaw > 0:
            yaw = yaw - 180
        else:
            yaw = yaw + 180
    else:
        print("Should not be here.")

    x = RADIUS * yaw * math.pi / 180
    y = RADIUS * math.tan(math.radians(pitch))
    fixation = [x, y]
    return fixation

if __name__ == "__main__":
    # create folder and clip video into frames
    video_2_image('./video_low_4s.mp4')

    ori_2_fixation(YAW, PITCH)

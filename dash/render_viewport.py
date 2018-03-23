import os
import cv2
import math
from PIL import Image

YAW     = -1.03605833333
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
        print "Read a new frame:", count
        count += 1 

def ori_2_fixation(yaw, pitch):
    # yaw boundary correction
    if yaw > 180:
        yaw = yaw % (-180)
    elif yaw < (-180):
        yaw = yaw % 180

    # pitch boundary correction
    if pitch > 90:
        pitch = pitch - 90
        if yaw > 0:
            yaw = yaw - 180
        else:
            yaw = 180 + yaw
    elif pitch < (-90):
        pitch = 0 - 180 - pitch
        if yaw > 0:
            yaw = yaw - 180
        else:
            yaw = 180 + yaw

    x = RADIUS * yaw * math.pi / 180
    y = RADIUS * math.tan(math.radians(pitch))

    # normalization
    if y > 959:
        y = 959
    if y < (-959):
        y = (-959)
    x_ori = x + 1920
    y_ori = (0 - y) + 960

    # left and right fixation point
    # the distance of left and right pupil is 65mm
    left_x_ori = x_ori - 50
    right_x_ori = x_ori + 50

    fixation = []
    fixation.append([round(left_x_ori), round(y_ori)])
    fixation.append([round(right_x_ori), round(y_ori)])
    return fixation

if __name__ == "__main__":
    # create folder and clip video into frames
    video_2_image('./video_low_4s.mp4')

    fixation = ori_2_fixation(YAW, PITCH)
    print(fixation)

#!/usr/bin/env python
#   Program:
#       A program to create viewing heatmap based on open viewing dataset
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.6.26

import os 
import sys
import cv2 
import numpy
import threading
import time
from multiprocessing import Process
from PIL import Image, ImageDraw
from libs import viewport

VIDEO = "game"
WIDTH = 3840
HEIGHT = 1920
FOV_DEGREEW = 100
FOV_DEGREEH = 100
TILE_W = 5
TILE_H = 5
heatmap_path = "./tmp_heatmap/"

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        print >> sys.stderr, 'Folder %s already exsits.' % path
        pass


def create_image(i, j):
    # Create a new image with the given size
    image = Image.new("RGB", (i, j))
    return image


def get_pixel(image, i, j):
    # inside image bounds or not 
    width, height = image.size 
    if i > width or j > height:
        return None
    # get pixel
    pixel = image.getpixel( (i, j) )
    return pixel


# ========================================================

class user_thread(Process):
    def __init__(self, userid, video, width, height, fov_degreew, fov_degreeh, tile_w, tile_h):
        #threading.Thread.__init__(self)
        super(user_thread, self).__init__()
        self.userid = userid
        self.video = video
        self.width = width
        self.height = height
        self.fov_degreew = fov_degreew
        self.fov_degreeh = fov_degreeh
        self.tile_w = tile_w
        self.tile_h = tile_h

    def run(self):
        HeatMap(self.userid, self.video, self.width, self.height, self.fov_degreew, self.fov_degreeh, self.tile_w, self.tile_h)


def HeatMap(userid, video, width, height, fov_degreew, fov_degreeh, tile_w, tile_h):
    try:
        user = open("./" + "user" + str(userid).zfill(2) + "_360dataset/sensory/orientation/" + video + "_user" + str(userid).zfill(2) + "_orientation.csv", "r")
        print >> sys.stderr, "Open: ./" + "user" + str(userid).zfill(2) + "_360dataset/sensory/orientation/" + video + "_user" + str(userid).zfill(2) + "_orientation.csv"
    except IOError as e:
        print >> sys.stderr, 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    except:
        print >> sys.stderr, "Unexpected error:", sys.exc_info()[0]

    user.readline()
    for i in range(1, 1801):
        if (os.path.isfile(heatmap_path + video + "_frame" + str(i).zfill(5) + ".png")):
            im = Image.open(heatmap_path + video + "_frame" + str(i).zfill(5) + ".png", "r")
        else:
            im = create_image(width, height)

        line = user.readline().strip().split(',')
        yaw = float(line[7])
        pitch = float(line[8])
        roll = float(line[9])
        (viewed_fov, probs) = viewport.ori_2_viewport(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

        pix = im.load()
        size = len(viewed_fov)
        for x in range(0, size):
            w = viewed_fov[x][0]
            h = viewed_fov[x][1]
            tmp = get_pixel(im, w, h)
            r = tmp[0]
            g = tmp[1]
            b = tmp[2]
            pix[w, h] = (r+5, g+5, b+5)

        im.save(heatmap_path + video + "_frame" + str(i).zfill(5) + ".png", "PNG")
        print >> sys.stderr, "user" + str(userid).zfill(2) + " --> " + heatmap_path + video + "_frame" + str(i).zfill(5) + ".png done."


make_sure_path_exists(heatmap_path)

for n in range(1, 51):
    user_thread(n, VIDEO, WIDTH, HEIGHT, FOV_DEGREEW, FOV_DEGREEH, TILE_W, TILE_H).start()
    #th1.start()
    time.sleep(60)

#user_thread(2, VIDEO, WIDTH, HEIGHT, FOV_DEGREEW, FOV_DEGREEH, TILE_W, TILE_H).start()
##th2.start()
#
#time.sleep(30)
#
#user_thread(3, VIDEO, WIDTH, HEIGHT, FOV_DEGREEW, FOV_DEGREEH, TILE_W, TILE_H).start()
##th3.start()

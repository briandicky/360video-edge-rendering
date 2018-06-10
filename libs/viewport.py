#!/usr/bin/env python
#   Program:
#       To render the viewport of a viewer.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.4.22

import os 
import sys 
import math 
import subprocess 
import cv2 
import time 
from libs import cal_prob
from libs import filemanager
from PIL import Image, ImageDraw

# Path
bitrate_path = "./bitrate/"
qp_path = "./qp/"
auto_path = "/auto/"
output_path = "./output/"
tmp_path = "./tmp/"
frame_path = "./frame/"

# Constants
FPS = 30
ENCODING_SERVER_ADDR = "140.114.77.170"

# ================================================================= #

def download_video_from_server(seg_length, seg_id, video):
    panorama = ENCODING_SERVER_ADDR + bitrate_path[1:] + str(seg_length) + "s" + "/" + str(video) + "/" + str(video) + "_equir_" + str(seg_id) + ".mp4"
    start_recv_ts = time.time()
    subprocess.call("wget %s -P %s" % (panorama, tmp_path), shell=True)
    return start_recv_ts


def ori_2_viewport(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    return cal_prob.gen_fov(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)


def video_2_image(seg_length, seg_id, video):
    # Check path and files existed or not
    filemanager.make_sure_path_exists(tmp_path)
    filemanager.make_sure_path_exists(output_path)
    filemanager.make_sure_path_exists(frame_path)

    # download the videos from encoding server
    #req_ts = time.time()
    #start_recv_ts = download_video_from_server(seg_length, seg_id, video)
    #end_recv_ts = time.time()

    # clip video into frames
    path = tmp_path + str(video) + "_equir_" + str(seg_id) + ".mp4"
    subprocess.call('mv %s %s' % (output_path + "output_" + str(seg_id) + ".mp4", path), shell=True)
    vidcap = cv2.VideoCapture(path)
    success, frame = vidcap.read()
    count = 1 
    success = True

    while success:
        # save frame as PNG format
        cv2.imwrite(frame_path + "frame%d.png" % count, frame)
        success, frame = vidcap.read()
        print "Clip a new frame:", count
        count += 1 

    #return (req_ts, start_recv_ts, end_recv_ts)


def render_fov_local(index, viewed_fov=[]):
    # open the image which can be many different formats
    ori_path = frame_path + "frame" + str(index) + ".png"
    im = Image.open(ori_path, "r")

    # get image size
    width, height = im.size

    # create new image and a pixel map
    new = create_image(width, height)
    pix = new.load()

    # get the pixel in viewport
    size = len(viewed_fov)
    for x in range(0, size, 1):
        i = viewed_fov[x][0]
        j = viewed_fov[x][1]
        pix[i, j] = get_pixel(im, i, j)

    path = tmp_path + "fov_temp" + str(index) + ".png" 
    new.save(path, "PNG")
    print >> sys.stderr, "frame" + str(index) + ": " + path + " done."


def concat_image_2_video(BITRATE, seg_id):
    # concatenate all the frame into one video
    #ffmpeg = "ffmpeg -framerate " + str(FPS) + " -y -i " + tmp_path + "fov_temp%d.png -c:v libx265 -preset:v ultrafast -crf 20 -pix_fmt yuv420p " + output_path + "output_%s.mp4" % seg_id
    ffmpeg = "ffmpeg -framerate " + str(FPS) + " -y -i " + tmp_path + "fov_temp%d.png -c:v libx265 -b:v %sM -preset:v ultrafast -pix_fmt yuv420p " % BITRATE + output_path + "output_%s.mp4" % seg_id
    subprocess.call(ffmpeg, shell=True)


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

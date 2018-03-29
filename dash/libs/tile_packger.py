#!/usr/bin/env python
#   Program:
#       To repackage and generate the equirectangular video from tiled videos.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.2

import os 
import sys 
import math 
import subprocess
from libs import cal_prob

# Path
bitrate_path = "./bitrate/"
qp_path = "./qp/"
auto_path = "/auto/"
output_path = "./output/"
tmp_path = "./tmp/"

# Constants
FPS = 30


def ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    # gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
    prob = cal_prob.gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

    tiles = []
    for i in range(0, len(prob), 1):
        if prob[i] == 1:
            tiles.append(i)

    corr_tiles = [j+2 for j in tiles]
    print(corr_tiles)
    return corr_tiles


def mixed_tiles_quality(no_of_tiles, seg_length, seg_id, 
        low=[], medium=[], high=[]):
    video_list = []
    video_list.append("dash_set1_init.mp4")
    print("dash_set1_init.mp4")

    # Sort the tracks into tiled videos list
    for i in range(1, no_of_tiles+2, 1):
        if i == 1:
            # track1 is needed
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in low:
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in medium:
            print("video_tiled_" + "medium_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "medium_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in high:
            print("video_tiled_" + "high_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "high_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        else:
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_"
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")

    make_sure_path_exists(tmp_path)
    make_sure_path_exists(output_path)
    clean_exsited_files(tmp_path, output_path, seg_id)

    # Concatenate init track and each tiled tracks
    for i in range(0, len(video_list), 1):
        subprocess.call('cat %s >> temp_%s.mp4' % 
                ( (bitrate_path + str(seg_length) + "s" + auto_path 
                    + video_list[i]), seg_id), shell=True)

    # Extract the raw hevc bitstream
    subprocess.call('MP4Box -raw 1 temp_%s.mp4' % seg_id, shell=True)

    # Repackage and generate new ERP video
    subprocess.call('MP4Box -add temp_%s_track1.hvc:fps=%s -inter 0 -new output_%s.mp4' % 
            (seg_id, FPS, seg_id), shell=True)

    # Move all the files into folders
    subprocess.call('mv temp_%s.mp4 %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv temp_%s_track1.hvc %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv output_%s.mp4 %s' % (seg_id, output_path), shell=True)


def only_fov_tiles(no_of_tiles, seg_length, seg_id, 
        low=[], medium=[], high=[]):
    video_list = []
    video_list.append("dash_set1_init.mp4")
    print("dash_set1_init.mp4")
                                                                     
    # Sort the tracks into tiled videos list
    for i in range(1, no_of_tiles+2, 1):
        if i == 1:
            # track1 is needed
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in low:
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in medium:
            print("video_tiled_" + "medium_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "medium_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in high:
            print("video_tiled_" + "high_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "high_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        else:
            print("video_tiled_" + "low_" + "dash_" + "track" + str(i) 
                    + "_" + str(seg_id) + ".m4s")
            video_list.append("video_tiled_" + "low_" + "dash_"
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
                                                                     
    # Concatenate init track and each tiled tracks
    for i in range(0, len(video_list), 1):
        subprocess.call('cat %s >> temp_%s.mp4' % 
                ( (bitrate_path + str(seg_length) + "s" + auto_path 
                    + video_list[i]), seg_id), shell=True)

    # Parse the viewed tile list to create remove list
    remove_track = []
    if low:
        for i in range(3, no_of_tiles+2, 1):
            if i not in low:
                remove_track.append("-rem %s" % i)
    elif medium:
        for i in range(3, no_of_tiles+2, 1):
            if i not in medium:
                remove_track.append("-rem %s" % i)
    elif high:
        for i in range(3, no_of_tiles+2, 1):
            if i not in high:
                remove_track.append("-rem %s" % i)
    else:
        print("It should not be here.")

    # convert reomve list to string
    cmd = ""
    for i in range(0, len(remove_track), 1):
        cmd = cmd + str(remove_track[i]) + " "

    # Check path and files existed or not
    make_sure_path_exists(tmp_path)
    make_sure_path_exists(output_path)
    clean_exsited_files(tmp_path, output_path, seg_id)

    # Remove unwatched tiles
    subprocess.call('MP4Box %s temp_%s.mp4 -out lost_temp_%s.mp4' % 
            (cmd, seg_id, seg_id), shell=True)

    # Extract the raw hevc bitstream
    subprocess.call('MP4Box -raw 1 lost_temp_%s.mp4' % seg_id, shell=True)

    # Repackage and generate new ERP video
    subprocess.call('MP4Box -add lost_temp_%s_track1.hvc:fps=%s -inter 0 -new output_%s.mp4' % 
            (seg_id, FPS, seg_id), shell=True)

    # Move all the files into folders
    subprocess.call('mv temp_%s.mp4 %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv lost_temp_%s.mp4 %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv lost_temp_%s_track1.hvc %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv output_%s.mp4 %s' % (seg_id, output_path), shell=True)


def ori_2_viewport(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    fixation = cal_prob.gen_fov(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
    return fixation


def render_fov_local(no_of_tiles, seg_length, seg_id, viewed_fov=[]):
    print("Under-construction: libs/tile_packger.py/render_fov_local")
    print(viewed_fov)
    print(len(viewed_fov))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Folder %s already exsits." % path)
        pass


def clean_exsited_files(tmp_path, output_path, seg_id):
    # Remove files at first
    try:
        rm_temp_mp4 = tmp_path + "temp_" + str(seg_id) + ".mp4" 
        os.remove(rm_temp_mp4)
    except OSError:
        print("File %s do not exsit." % rm_temp_mp4)
        pass

    try:
        rm_temp_hvc = tmp_path + "temp_" + str(seg_id) + "_track1.hvc"
        os.remove(rm_temp_hvc)
    except OSError:
        print("File %s do not exsit." % rm_temp_hvc)
        pass 

    try:
        rm_output = output_path + "output_" + str(seg_id) + ".mp4"
        os.remove(rm_output)
    except OSError:
        print("File %s do not exsit." % rm_output)
        pass

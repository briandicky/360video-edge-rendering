#!/usr/bin/env python
#   Program:
#       To render the equirectangular video from tiled videos.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.2

import os 
import sys 
import math 
import subprocess
import time
from libs import cal_prob
from libs import filemanager

# Path
bitrate_path = "./bitrate/"
qp_path = "./qp/"
auto_path = "/auto/"
output_path = "./output/"
tmp_path = "./tmp/"
frame_path = "./frame/"

# Constants
FLAG = 1
FPS = 30
ENCODING_SERVER_ADDR = "140.114.77.170"

# ================================================================= #

def ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h):
    # gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
    prob = cal_prob.gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

    tiles = []
    for i in range(0, len(prob), 1):
        if prob[i] == 1:
            tiles.append(i)

    corr_tiles = [j+2 for j in tiles]
    print >> sys.stderr, corr_tiles
    return corr_tiles


def mixed_tiles_quality(no_of_tiles, seg_length, user_id, seg_id, VIDEO, bitrate, mode,low=[], medium=[], high=[]):
    # Check path and files existed or not
    global tmp_path
    tmp_path = "./tmp_"+ VIDEO + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate +'_'+ mode+ '/'
    global output_path
    output_path = "./output_"+ VIDEO + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate+'_' + mode+ '/'
    
    filemanager.make_sure_path_exists(tmp_path)
    filemanager.make_sure_path_exists(output_path)
    filemanager.clean_exsited_files(tmp_path, output_path, seg_id)

    # Create a list to store all the videos
    video_list = []
    video_list.append("dash_set1_init.mp4")
    print >> sys.stderr, 'dash_set1_init.mp4'

    # Sort the tracks into tiled videos list
    BR = bitrate+'_'
    for i in range(1, no_of_tiles+2, 1):
        if i == 1:
            # track1 is needed
            debug_msg = "video_tiled_" + "1Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "1Mbps_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in low:
            debug_msg = "video_tiled_" + BR + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + BR + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in medium:
            debug_msg = "video_tiled_" + BR + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + BR + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in high:
            debug_msg = "video_tiled_" + BR + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + BR + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        else:
            debug_msg = "video_tiled_" + BR + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + BR + "dash_"
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")

    # download the videos from encoding server
    req_ts = time.time()
    start_recv_ts = download_tiled_video_from_server(VIDEO, no_of_tiles, seg_length, video_list)
    end_recv_ts = time.time()
    
    # Concatenate init track and each tiled tracks
    offset = VIDEO + '_user'+ user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode
    for i in range(0, len(video_list), 1):
        subprocess.call('cat %s >> temp_%s.mp4' % 
                ( (tmp_path + video_list[i]), offset), shell=True)

    # Extract the raw hevc bitstream
    subprocess.call('MP4Box -raw 1 temp_%s.mp4' % offset, shell=True)

    # Repackage and generate new ERP video
    subprocess.call('MP4Box -add temp_%s_track1.hvc:fps=%s -inter 0 -new output_%s.mp4' % 
            ( offset, FPS, offset), shell=True)

    # Move all the files into folders
    subprocess.call('mv temp_%s.mp4 %s' % ( offset, tmp_path), shell=True)
    subprocess.call('mv temp_%s_track1.hvc %s' % ( offset, tmp_path), shell=True)
    subprocess.call('mv output_%s.mp4 %s' % ( offset, output_path), shell=True)
    return (req_ts, start_recv_ts, end_recv_ts)


def only_fov_tiles(no_of_tiles, seg_length, seg_id, VIDEO,
        low=[], medium=[], high=[]):
    # Check path and files existed or not
    filemanager.make_sure_path_exists(tmp_path)
    filemanager.make_sure_path_exists(output_path)
    filemanager.clean_exsited_files(tmp_path, output_path, seg_id)

    video_list = []
    video_list.append("dash_set1_init.mp4")
    print >> sys.stderr, 'dash_set1_init.mp4'
                                                                     
    # Sort the tracks into tiled videos list
    for i in range(1, no_of_tiles+2, 1):
        if i == 1:
            # track1 is needed
            debug_msg = "video_tiled_" + "1Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "1Mbps_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in low:
            debug_msg = "video_tiled_" + "2Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "2Mbps_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in medium:
            debug_msg = "video_tiled_" + "2Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "2Mbps_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in high:
            debug_msg = "video_tiled_" + "2Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "2Mbps_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        else:
            debug_msg = "video_tiled_" + "2Mbps_" + "dash_" + "track" + str(i) + "_" + str(seg_id) + ".m4s"
            #print >> sys.stderr, debug_msg
            video_list.append("video_tiled_" + "2Mbps_" + "dash_"
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
                                                                     
    # download the videos from encoding server
    req_ts = time.time()
    start_recv_ts = download_tiled_video_from_server(VIDEO, no_of_tiles, seg_length, video_list)
    end_recv_ts = time.time()

    # Concatenate init track and each tiled tracks
    for i in range(0, len(video_list), 1):
        subprocess.call('cat %s >> temp_%s.mp4' % 
                ( (tmp_path + video_list[i]), seg_id), shell=True)

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
        print >> sys.stderr, "It should not be here."

    # convert reomve list to string
    cmd = ""
    for i in range(0, len(remove_track), 1):
        cmd = cmd + str(remove_track[i]) + " "

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
    return (req_ts, start_recv_ts, end_recv_ts)


def download_tiled_video_from_server(VIDEO, no_of_tiles, seg_length, video_list=[]):
    starting_download = True
    for line in video_list:
        if no_of_tiles == 3*3:
            tile = ENCODING_SERVER_ADDR + bitrate_path[1:] + str(seg_length) + "s" + "/" + VIDEO + auto_path + "3x3/" + line
        elif no_of_tiles == 5*5:
            tile = ENCODING_SERVER_ADDR + bitrate_path[1:] + str(seg_length) + "s" + "/" + VIDEO + auto_path + "5x5/" + line
        else:
            print >> sys.stderr, "Wrong NO_OF_TILES, please check it out."

        try:
            rm_tile = tmp_path + line
            os.remove(rm_tile)
        except OSError:
            print >> sys.stderr, 'File %s do not exsit.' % rm_tile
            pass

        # record the starting download time
        if starting_download:
            start_recv_ts = time.time()
            starting_download = False

        subprocess.call("wget %s -P %s" % (tile, tmp_path), shell=True)

    return start_recv_ts

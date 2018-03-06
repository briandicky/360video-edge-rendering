#!/usr/bin/env python
#   Program:
#       To repackage and generate the equirectangular video from tiled videos.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.2

import os
import sys
import subprocess
import argparse
import math

no_of_tiles = 3*3
ip_encoding_server = "140.114.77.125"
length_dash_segment = 10

bitrate_prefix = "./bitrate/"
qp_prefix = "./qp/"
auto_prefix = "/auto/"
output_prefix = "./output/"

#subprocess('cat dash_tiled_set1_init.mp4 >> tiled.mp4', shell=True)

#video_tiled_medium_dash_track1_1.m4s video_tiled_medium_dash_track2_1.m4s video_tiled_medium_dash_track3_1.m4s video_tiled_medium_dash_track4_1.m4s video_tiled_medium_dash_track5_1.m4s ../low/video_tiled_low_dash_track6_1.m4s video_tiled_medium_dash_track7_1.m4s video_tiled_medium_dash_track8_1.m4s video_tiled_medium_dash_track9_1.m4s video_tiled_medium_dash_track10_1.m4s > test.mp4

parser = argparse.ArgumentParser(
        prog='tiles_repackager',
        description='blablabla',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--ip', nargs='?', default=ip_encoding_server, help='The ip address of the encoding server')
parser.add_argument('--tiles', nargs='?', type=int, default=no_of_tiles, help='The total number of tiles')
parser.add_argument('--bitrate', action='store_true', help='Tiles adaptation based on bitrate')
parser.add_argument('--segment', nargs='+', type=int, help='The id of dash segment')
parser.add_argument('--low', nargs='*', type=int, metavar='2 3 4', help='Set down which tiles should be low quality')
parser.add_argument('--medium', nargs='*', type=int, metavar='5 6 7', help='Set down which tiles should be medium quality')
parser.add_argument('--high', nargs='*',  type=int, metavar='8 9 10', help='Set down which tiles should be high quality')

args = parser.parse_args('--bitrate --segment 1 --low 2 3 4 --medium 5 6 7 --high 8 9 10'.split())

#parser.print_help()
#print()
#print(args.ip)
#print(args.tiles)
#print(args.bitrate)
#print(args.segment)
#print(args.low)
#print(args.medium)
#print(args.high)

# add init track into tiled videos list
video_list = []
video_list.append("dash_tiled_set1_init.mp4")

# Sort the tracks into tiled videos list
for i in range(1, no_of_tiles+2, 1):
    if i == 1:
        # track1 is needed
        video_list.append("video_tiled_" + "low_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    elif i in args.low:
        video_list.append("video_tiled_" + "low_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    elif i in args.medium:
        video_list.append("video_tiled_" + "medium_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    elif i in args.high:
        video_list.append("video_tiled_" + "high_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    else:
        print("There is no case.")
#print()

# Remove files at first
try:
    rm_temp_mp4 = "temp_" + str(args.segment[0]) + ".mp4" 
    os.remove(rm_temp_mp4)
except OSError:
    print ("File %s do not exsit." % rm_temp_mp4)
    pass

try:
    rm_temp_hvc = "temp_" + str(args.segment[0]) + "_track1.hvc"
    os.remove(rm_temp_hvc)
except OSError:
    print ("File %s do not exsit." % rm_temp_hvc)
    pass 

try:
    rm_output = "output_" + str(args.segment[0]) + ".mp4"
    os.remove(rm_output)
except OSError:
    print ("File %s do not exsit." % rm_output)
    pass

# Concatenate init track and each tiled tracks
for i in range(0, len(video_list), 1):
    subprocess.call('cat %s >> temp_%s.mp4' % 
            ( (bitrate_prefix + str(length_dash_segment) + "s" + auto_prefix + video_list[i]), 
                args.segment[0]), shell=True)

# Extract the raw hevc bitstream
subprocess.call('MP4Box -raw 1 temp_%s.mp4' % args.segment[0], shell=True)

# Repackage and generate new ERP video
subprocess.call('MP4Box -add temp_%s_track1.hvc:fps=25 -new output_%s.mp4' % 
        (args.segment[0], args.segment[0]), shell=True)

# End

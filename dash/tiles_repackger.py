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

parser.print_help()
args = parser.parse_args('--bitrate --segment 1 --low 2 3 4 --medium 5 6 7 --high 8 9 10'.split())

print()
print(args.ip)
print(args.tiles)
print(args.bitrate)
print(args.segment)
print(args.low)
print(args.medium)
print(args.high)

# add init track into tiled videos list
video_list = []
video_list.append("dash_tiled_set1_init.mp4")

# Sort the tracks into tiled videos list
for i in range(1, no_of_tiles+2, 1):
    if i in args.low:
        print("video_tiled_" + "low_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
        video_list.append("video_tiled_" + "low_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    elif i in args.medium:
        print("video_tiled_" + "medium_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
        video_list.append("video_tiled_" + "medium_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    elif i in args.high:
        print("video_tiled_" + "high_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
        video_list.append("video_tiled_" + "high_" + "dash_" + "track" + str(i) + "_" + str(args.segment[0]) + ".m4s")
    else:
        print("There is no case.")
print()

# Concatenate init track and each tiled tracks
for i in range(0, len(video_list), 1):
    print(bitrate_prefix + str(length_dash_segment) + "s" + auto_prefix + video_list[i])
    subprocess.call('ls %s' % (bitrate_prefix + str(length_dash_segment) + "s" + auto_prefix + video_list[i]), shell=True)


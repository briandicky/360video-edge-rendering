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
ip_encoding_server = '140.114.77.125'
dash_segment = 10

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
parser.add_argument('--segment', nargs='?', type=int, default=dash_segment, help='The length (in secs) of dash segment')
parser.add_argument('--low', nargs='*', type=int, metavar='2 3 4', help='Set down which tiles should be low quality')
parser.add_argument('--medium', nargs='*', type=int, metavar='5 6 7', help='Set down which tiles should be medium quality')
parser.add_argument('--high', nargs='*',  type=int, metavar='8 9 10', help='Set down which tiles should be high quality')

args = parser.parse_args('--bitrate --low 1 2 3 --medium 4 5 6 --high 7 8 9'.split())

print (args.ip)
print (args.tiles)
print (args.bitrate)
print (args.segment)
print (args.low)
print (args.medium)
print (args.high)

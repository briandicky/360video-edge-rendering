#!/usr/bin/env python
#   Program:
#       TBD.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.6

import os 
import sys
import math
from libs import tile_packger 
from libs import cal_prob

# viewing domain arguments
yaw = float(sys.argv[1])
pitch = float(sys.argv[2])
fov_degreew = 100
fov_degreeh = 100
tile_w = 3
tile_h = 3

print("yaw: %s" % yaw)
print("pithc: %s" % pitch)
print("fov_degreew: %s" % fov_degreew)
print("fov_degreeh: %s" % fov_degreeh)
print("tile_w: %s" % tile_w)
print("tile_h: %s" % tile_h)
print

# Compressed domain arguments
no_of_tiles = tile_w*tile_h
ip_encoding_server = "140.114.77.125"
seg_length = 10
seg_id = int(sys.argv[3])

print("no_of_tiles: %s" % no_of_tiles)
print("seg_length: %s" % seg_length)
print("seg_id: %s" % seg_id)


viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
tile_packger.mixed_tiles_quality(no_of_tiles, seg_length, seg_id, [], [], viewed_tiles)

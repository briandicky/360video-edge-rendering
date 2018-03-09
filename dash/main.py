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
from cal_prob import gen_prob
import tile_packger

# viewing domain arguments
yaw = float(sys.argv[1])
pitch = float(sys.argv[2])
fov_degreew = 100
fov_degreeh = 100
tile_w = 3
tile_h = 3

print(yaw)
print(pitch)
print(fov_degreew)
print(fov_degreeh)
print(tile_w)
print(tile_h)

# Compressed domain arguments
no_of_tiles = tile_w*tile_h
ip_encoding_server = "140.114.77.125"
seg_length = 10

# gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
prob = gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

tiles = []
for i in range(0, len(prob), 1):
    if prob[i] == 1:
        tiles.append(i)

viewed_tiles = [j+2 for j in tiles]
print(viewed_tiles)

tile_packger.mixed_tiles_quality(9, 10, 1, [], [], viewed_tiles)

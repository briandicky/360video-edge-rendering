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
print()

# Compressed domain arguments
no_of_tiles = tile_w*tile_h
ip_encoding_server = "140.114.77.125"
length_dash_segment = 10

bitrate_prefix = "./bitrate/"
qp_prefix = "./qp/"
auto_prefix = "/auto/"
output_prefix = "./output/"

# gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
prob = gen_prob(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

print(prob)

tiles = []
for i in range(0, len(prob), 1):
    if prob[i] == 1:
        tiles.append(i)

print(tiles)

new_tiles = [j+2 for j in tiles]
print(new_tiles)

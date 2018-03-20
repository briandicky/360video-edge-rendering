#!/usr/bin/env python
#   Program:
#       A program to test the functions in this project.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.17

import os 
import sys 
from libs import cal_prob
from libs import tile_packger

# viewing constants
MODE_MIXED = 1
MODE_FOV = 0
MODE_RENDER = 0
yaw = -120.03605833333
pitch = 0.103563888889
roll = -3.993
fov_degreew = 100
fov_degreeh = 100
tile_w = 3
tile_h = 3

# compressed domain constants
NO_OF_TILES = tile_w*tile_h
SEG_LENGTH = 10
SEG_ID = 3

# calculate viewer's orientation and repackage tiled video
viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

if MODE_MIXED:
    tile_packger.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
elif MODE_FOV:
    tile_packger.only_fov_tiles(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
elif MODE_RENDER:
    tile_packger.render_fov_local(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
else:
    print("GGGGGGGGGGGGG")
    exit(0)

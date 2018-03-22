#!/usr/bin/env python
#   Program:
#       A program to test the functions in this project.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.17

import os 
import sys 
from libs import tile_packger

# Mode 
MODE_MIXED = 0
MODE_FOV = 0
MODE_RENDER = 1

# viewing constants
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
if MODE_MIXED:
    viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
elif MODE_FOV:
    viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
elif MODE_RENDER:
    viewed_tiles = tile_packger.ori_2_viewport(yaw, pitch, fov_degreew, fov_degreeh)
else:
    print("GGGGGGGGGGGGG at calculating orientation")
    exit(0)

if MODE_MIXED:
    tile_packger.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
elif MODE_FOV:
    tile_packger.only_fov_tiles(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
elif MODE_RENDER:
    tile_packger.render_fov_local(NO_OF_TILES, SEG_LENGTH, SEG_ID, [], viewed_tiles, [])
else:
    print("GGGGGGGGGGGGG at tile repackging")
    exit(0)

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
import socket
import time
from libs import tile_packger 
from libs import cal_prob

# viewing constants
#yaw = 
#pitch = 
#roll =
fov_degreew = 100
fov_degreeh = 100
tile_w = 3
tile_h = 3

# socket constants
SERVER_ADDR = "140.114.77.125"
SERVER_PORT = 9487
CHUNK_SIZE = 4096

# compressed domain constants
NO_OF_TILES = tile_w*tile_h
seg_length = 10
seg_id = 3

f = open("record.csv", "w")
f.write("serverip,serverport,serverts,clientip,clientport,clientts,segid,rawYaw,rawPitch,rawRoll\n")
# End of constants

#viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
#tile_packger.mixed_tiles_quality(no_of_tiles, seg_length, seg_id, [], [], viewed_tiles)


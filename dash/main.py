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
SEG_LENGTH = 10
#seg_id = 3

f = open("record.csv", "w")
f.write("serverip,serverport,serverts,clientip,clientport,clientts,segid,rawYaw,rawPitch,rawRoll\n")
# End of constants

#viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
#tile_packger.mixed_tiles_quality(no_of_tiles, SEG_LENGTH, seg_id, [], [], viewed_tiles)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection 
    print >> sys.stderr, 'waiting for a connection...' 
    connection, client_address = sock.accept()
    try:
        #print >> sys.stderr, 'connection:', connection
        print >> sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(CHUNK_SIZE)
            print >> sys.stderr, 'received "%s"' % data
            
            if data:
                # server info
                f.write(str(SERVER_ADDR) + ",")
                f.write(str(SERVER_PORT) + ",")
                ts = time.time()
                f.write(str(ts) + ",")

                # client info
                f.write(str(client_address[0]) + "," + str(client_address[1]) + ",")
                ori = data.split(",")
                f.write(str(ori[0]) + "," + str(ori[1]) + "," + str(ori[2]) + "," 
                        + str(ori[3]) + "," + str(ori[4]))

                seg_id = int(ori[1])
                yaw = float(ori[2])
                pitch = float(ori[3])
                roll = float(ori[4])
                print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
                viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

                print >> sys.stderr, '\nrepackging different quality tiles track into ERP mp4 video...'
                tile_packger.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, seg_id, [], viewed_tiles, [])

                print >> sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >> sys.stderr, 'no more data from', client_address
                break
    finally:
        # Clean up the connection
        connection.close()

#!/usr/bin/env python
#   Program:
#       A program handles TCPSocket, listen command from clients, and render the vr view.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.6

import os 
import sys
import math
import socket
import time 
import errno
import struct
import pickle
from socket import error as SocketError
from libs import tile_packger 

# viewing constants
MODE_MIXED = 1
MODE_FOV = 0
MODE_RENDER = 0
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

# debugging messages 
print >> sys.stderr, "No. of tiles = %s x %s = %s" % (tile_w, tile_h, NO_OF_TILES)
print >> sys.stderr, "FoV width = %s, FoV height = %s" % (fov_degreew, fov_degreeh)
print >> sys.stderr, "Segment length = %s sec\n" % SEG_LENGTH

f = open("record.csv", "w")
f.write("serverip,serverport,serverts,clientip,clientport,clientts,segid,rawYaw,rawPitch,rawRoll\n")
# End of constants

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
# Specifies the maximum number of queued connections (usually 5)
sock.listen(5)

while True:
    # Wait for a connection 
    print >> sys.stderr, 'waiting for a connection...' 
    connection, client_address = sock.accept()
    try:
        #print >> sys.stderr, 'connection:', connection
        print >> sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
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
            f.write("\n")

            # calculate orientation and repackage tiled video
            seg_id = int(ori[1])
            yaw = float(ori[2])
            pitch = float(ori[3])
            roll = float(ori[4])
            print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
            viewed_tiles = tile_packger.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)

            # MODE_MIXED: mixed different quality tiles 
            # MODE_FOV: only viewed tiles 
            # MODE_RENDER: TBD.
            print >> sys.stderr, '\nrepackging different quality tiles track into ERP mp4 format...'
            if MODE_MIXED:
                tile_packger.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, seg_id, [], viewed_tiles, [])
            elif MODE_FOV:
                tile_packger.only_fov_tiles(NO_OF_TILES, SEG_LENGTH, seg_id, [], viewed_tiles, [])
            elif MODE_RENDER:
                tile_packger.render_fov_local(NO_OF_TILES, SEG_LENGTH, seg_id, [], viewed_tiles, [])
            else:
                print("GGGGGGGGGGGGG")
                exit(0)

            # sending ERP mp4 format video back to client
            print >> sys.stderr, '\nsending video back to the client'
            path_of_video = "./output/" + "output_" + str(seg_id) + ".mp4"
            video = open(path_of_video).read() 
            # seperate video into samll chunks then transmit each of them
            #count = 0
            #while count < len(video):
            #    chunk = video[count:count+CHUNK_SIZE]
            #    connection.sendall(chunk)
            #    count += CHUNK_SIZE
            print >> sys.stderr, 'finished sending video\n'
            connection.sendall(video)
            connection.close()
        else:
            print >> sys.stderr, 'no more data from\n', client_address
            break
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise # Not error we are looking for
        pass # Handle error here.
    finally:
        # Clean up the connection
        connection.close()

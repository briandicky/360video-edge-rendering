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
import signal
from enum import Enum
from libs import tiled
from libs import viewport
from socket import error as SocketError

# viewing constants
class RENDER(Enum):
    CR = 1
    TR = 2
    VPR = 3
    TR_only = 4

# set rendering mode here
MODE = RENDER.VPR

fov_degreew = 100
fov_degreeh = 100
tile_w = 3
tile_h = 3

# socket constants
ENCODING_SERVER_ADDR = "140.114.77.170"
ENCODING_SERVER_PORT = 80
EDGE_SERVER_ADDR = "140.114.77.125"
EDGE_SERVER_PORT = 9487
CHUNK_SIZE = 4096

# compression constants
NO_OF_TILES = tile_w*tile_h
SEG_LENGTH = 4
FPS = 30

# metadata constants
#VIDEO = "game"
#ORIENTATION = "./game_user03_orientation.csv"

# debugging messages 
print >> sys.stderr, "No. of tiles = %s x %s = %s" % (tile_w, tile_h, NO_OF_TILES)
print >> sys.stderr, "FoV width = %s, FoV height = %s" % (fov_degreew, fov_degreeh)
print >> sys.stderr, "Segment length = %s sec\n" % SEG_LENGTH

# open the file for output messages
f = open("./log.csv", "w")
f.write("cloudip,cloudport,edgeip,edgeport,clientip,clientport,segid,Yaw,Pitch,Roll,clienreqts,edgerecv,edgereqts,edgestartrecvts,edgeendrecvts,clientrecvts,filesize(bytes)\n")

# user orientation log file
#user = open(ORIENTATION, "r")
# End of constants

# signal handler
def handler_sigint(signum, frame): 
    print >> sys.stderr, 'KeyboardInterrupt, then close files and clean up all the connections'
    f.close()
    exit(0)

def handler_sigterm(signum, frame):
    print >> sys.stderr, 'Killed by user, then close files and clean up all the connections'
    f.close()
    exit(0)

signal.signal(signal.SIGINT, handler_sigint)
signal.signal(signal.SIGTERM, handler_sigterm)
# end of signal handler

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (EDGE_SERVER_ADDR, EDGE_SERVER_PORT)
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
        edgerecvts = time.time()
        print >> sys.stderr, 'received "%s"' % data
        
        if data:
            # process the data receved from client
            ori = data.split(",")

            # calculate orientation and repackage tiled video
            seg_id = int(ori[1])
            yaw = float(ori[2])
            pitch = float(ori[3])
            roll = float(ori[4])
            VIDEO = str(ori[5])
            ORIENTATION = str(ori[6])

            if MODE.name == "TR":
                print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
                viewed_tiles = tiled.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
            elif MODE.name == "TR_only":
                print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
                viewed_tiles = tiled.ori_2_tiles(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
            elif MODE.name == "VPR":
                viewed_tiles = []
                for i in range(1, (tile_w*tile_h + 2), 1):
                    viewed_tiles.append(i)
            elif MODE.name == "CR":
                viewed_tiles = []
                for i in range(1, (tile_w*tile_h + 2), 1):
                    viewed_tiles.append(i)
            else:
                print >> sys.stderr, 'GGGGGGGGGGGGG'
                exit(0)

            # CR: do nothing
            # TR: mixed different quality tiles 
            # TR_only: only viewed tiles 
            # VPR: only render the pixels in user's viewport
            print >> sys.stderr, '\nencapsulating different quality tiles track into ERP mp4 format...'
            if MODE.name == "TR":
                (reqts, start_recvts, end_recvts) = tiled.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, seg_id, VIDEO, [], viewed_tiles, [])
            elif MODE.name == "TR_only":
                (reqts, start_recvts, end_recvts) = tiled.only_fov_tiles(NO_OF_TILES, SEG_LENGTH, seg_id, VIDEO, [], viewed_tiles, [])
            elif MODE.name == "VPR":
                (reqts, start_recvts, end_recvts) = tiled.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, seg_id, VIDEO, [], viewed_tiles, [])

                viewport.video_2_image(SEG_LENGTH, seg_id, VIDEO)

                print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_fov]...'               
                # read the user orientation file and skip the first line
                # then, calculate the pixel viewer by user and render the viewport
                # no_frames = SEG_LENGTH * FPS

                try:
                    user = open("./360dataset/sensory/orientation/" + ORIENTATION, "r")
                except IOError as e:
                    print >> sys.stderr, 'I/O error({0}): {1}'.format(e.errno, e.strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise

                user.readline()
                #for i in range(1, SEG_LENGTH * FPS + 1, 1):
                for i in range(1, 65, 1):
                    line = user.readline().strip().split(',')
                    yaw = float(line[7])
                    pitch = float(line[8])
                    roll = float(line[9])
                    #print >> sys.stderr, line[7], line[8], line[9]
                    viewed_fov = viewport.ori_2_viewport(yaw, pitch, fov_degreew, fov_degreeh, tile_w, tile_h)
                    viewport.render_fov_local(i, viewed_fov)

                # concatenate all the frame into one video
                viewport.concat_image_2_video(seg_id)
                user.close()
            elif MODE.name == "CR":
                (reqts, start_recvts, end_recvts) = tiled.mixed_tiles_quality(NO_OF_TILES, SEG_LENGTH, seg_id, VIDEO, [], viewed_tiles, [])
            else:
                print >> sys.stderr, 'GGGGGGGGGGGGG'
                exit(0)

            # sending ERP mp4 format video back to client
            print >> sys.stderr, '\nsending video back to the client'
            path_of_video = "./output/" + "output_" + str(seg_id) + ".mp4"
            video = open(path_of_video).read() 
            video_size = os.path.getsize(path_of_video)
            connection.sendall(video)
            clientrecvts = time.time()
            # seperate video into small chunks then transmit each of them
            #count = 0
            #while count < len(video):
            #    chunk = video[count:count+CHUNK_SIZE]
            #    connection.sendall(chunk)
            #    count += CHUNK_SIZE
            print >> sys.stderr, 'finished sending video\n'
            connection.close()

            # cloud server info 
            f.write(str(ENCODING_SERVER_ADDR) + ",")
            f.write(str(ENCODING_SERVER_PORT) + ",")

            # edge server info
            f.write(str(EDGE_SERVER_ADDR) + ",")
            f.write(str(EDGE_SERVER_PORT) + ",")
        
            # edn client info
            f.write(str(client_address[0]) + "," + str(client_address[1]) + ",")
            f.write(str(ori[1]) + "," + str(ori[2]) + "," + str(ori[3]) + "," + str(ori[4]) + ",")

            # edge/client request and recv time 
            # (clienreqts,edgerecvts,edgereqts,edgestartrecvts,edgeendrecvts,clientrecvts,filesize")
            f.write(str(ori[0]) + ",") # clientreqts
            f.write(str(format(edgerecvts, '.6f')) + ",") # edgerecvts
            f.write(str(format(reqts, '.6f')) + "," + str(format(start_recvts, '.6f')) + "," + str(format(end_recvts, '.6f')) + ",") # edgereqts, edgestartrecvts, edgeendrecvts
            f.write(str(format(clientrecvts, '.6f')) + ",") # clientrecvts
            f.write(str(video_size)) # total file that are transferred to client
            f.write("\n")
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

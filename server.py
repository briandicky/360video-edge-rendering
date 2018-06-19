#!/usr/bin/env python
#   Program:
#       A program handles TCPSocket, listen command from clients, and render the vr view.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.6

import os
import shutil 
import sys
import math
import socket
import time 
import errno
import struct
import cPickle
import signal
import subprocess
import cv2
import threading
from multiprocessing import Process
from enum import Enum
from libs import tiled
from libs import viewport
from libs import VPsnrCalc
from libs import PsnrCalc_tiled
from libs import filemanager
from socket import error as SocketError


class Server(Process):
    fov_degree_w = 100
    fov_degree_h = 100
    tile_w = 5
    tile_h = 5
    # socket constants
    ENCODING_SERVER_ADDR = "140.114.77.170"
    ENCODING_SERVER_PORT = 80
    CHUNK_SIZE = 4096
    # compression constants
    SEG_LENGTH = 4
    FPS = 30

    psnr_path = "./PSNR/"
    pkl_path = "./pickles/"
    log_path = "./log/"
    # viewing constants

    def __init__( self, edge_server_addr, edge_server_port):
	super(Server, self).__init__()
	self.NO_OF_TILES = self.tile_w * self.tile_h
	self.EDGE_SERVER_ADDR = edge_server_addr
	self.EDGE_SERVER_PORT = edge_server_port


    def run( self):

	# debugging messages 
	print >> sys.stderr, "No. of tiles = %s x %s = %s" % (self.tile_w, self.tile_h, self.NO_OF_TILES)
	print >> sys.stderr, "FoV width = %s, FoV height = %s" % (self.fov_degree_w, self.fov_degree_h)
	print >> sys.stderr, "Segment length = %s sec\n" % self.SEG_LENGTH

        filemanager.make_sure_path_exists(self.psnr_path)
        filemanager.make_sure_path_exists(self.pkl_path)
        filemanager.make_sure_path_exists(self.log_path)

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = (self.EDGE_SERVER_ADDR, self.EDGE_SERVER_PORT)
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
		#shutil.rmtree("tmp/")

		# Receive the data in small chunks and retransmit it
		data = connection.recv(self.CHUNK_SIZE)
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
		    user_id = ori[6]
		    #ORIENTATION = str(ori[6])
		    mode = str(ori[7])
		    bitrate = str(ori[8])
		    
		    ORIENTATION = VIDEO+'_user'+user_id+"_orientation.csv"
		    if mode == "TR":
			print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
			viewed_tiles = tiled.ori_2_tiles(yaw, pitch, self.fov_degree_w, self.fov_degree_h, self.tile_w, self.tile_h)
		    elif mode == "TR_only":
			print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_tiles]...'
			viewed_tiles = tiled.ori_2_tiles(yaw, pitch, self.fov_degree_w, self.fov_degree_h, self.tile_w, self.tile_h) #100 100 5 5
		    elif mode == "VPR":
			viewed_tiles = []
			for i in range(1, (self.tile_w*self.tile_h + 2), 1):
			    viewed_tiles.append(i)
		    elif mode == "CR":
			viewed_tiles = []
			for i in range(1, (self.tile_w*self.tile_h + 2), 1):
			    viewed_tiles.append(i)
		    else:
			print >> sys.stderr, 'GGGGGGGGGGGGG'
			exit(0)

		    # CR: do nothing
		    # TR: mixed different quality tiles 
		    # TR_only: only viewed tiles 
		    # VPR: only render the pixels in user's viewport
		    print >> sys.stderr, '\nencapsulating different quality tiles track into ERP mp4 format...'

		    repo = "output_" + VIDEO + '_user'+ user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode + "/"
	            the_file = "output_" + VIDEO + '_user'+ user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode + ".mp4"
		    psnr_list = []
		    psnr_name = "./PSNR/psnr_"+VIDEO + '_user'+ user_id+ '_' + str(seg_id)+'_'+bitrate+'_'+mode+".csv"
		    if mode == "TR":
			(reqts, start_recvts, end_recvts) = tiled.mixed_tiles_quality(self.NO_OF_TILES, self.SEG_LENGTH, user_id, seg_id, VIDEO, bitrate, mode, [], viewed_tiles, [])
			expe = cv2.VideoCapture(repo + the_file)
			cont = cv2.VideoCapture("./360videos_60s/"+VIDEO+"_equir.mp4")
			frame_no = (seg_id - 1)*64 + 1
			for i in range(frame_no-1):
			    ret, imgC = cont.read()
			while(True):
			    ret, imgE = expe.read()
			    if(imgE is None):
				print >> sys.stderr, "next clip..."
				break
			    ret, imgC = cont.read()
			    if(imgC is None):
				print >> sys.stderr, "Error occured. Cannot read the video."
				break
			    psnr = PsnrCalc_tiled.PsnrTiledCalc(imgE, imgC, viewed_tiles)
			    print(str(frame_no)+" tiled_psnr:          "+str(psnr))
			    psnr_list.append(psnr)
			    
			    f = open(psnr_name, "a")
			    f.write(str(frame_no).ljust(15)+',')
			    f.write(str(psnr).rjust(15))
			    f.write('\n')
			    f.close()
			    frame_no += 1
			    #if( (frame_no%T) != 0 or frame_no < next_frame):
			    #    frame_no += 1
			    #    continue
		        f = open(psnr_name, "a")
			f.write("avg_psnr, ")
			f.write(str(sum(psnr_list)/len(psnr_list)))
			f.write('\n')
			f.close()
			    
		    elif mode == "TR_only":
			(reqts, start_recvts, end_recvts) = tiled.only_fov_tiles(self.NO_OF_TILES, self.SEG_LENGTH, seg_id, VIDEO, bitrate, [], viewed_tiles, [])
		    elif mode == "VPR":
			(reqts, start_recvts, end_recvts) = tiled.mixed_tiles_quality(self.NO_OF_TILES, self.SEG_LENGTH, user_id, seg_id, VIDEO, bitrate, mode, [], viewed_tiles, [])

			viewport.video_2_image(self.SEG_LENGTH, user_id, seg_id, VIDEO, bitrate)

			print >> sys.stderr, '\ncalculating orientation from [yaw, pitch, roll] to [viewed_fov]...'               
			# read the user orientation file and skip the first line
			# then, calculate the pixel viewer by user and render the viewport
			# no_frames = self.SEG_LENGTH * self.FPS

			try:
			    user = open("./360dataset/sensory/orientation/" + ORIENTATION, "r")
			except IOError as e:
			    print >> sys.stderr, 'I/O error({0}): {1}'.format(e.errno, e.strerror)
			except:
			    print "Unexpected error:", sys.exc_info()[0]
			    raise

			user.readline()
			for i in range(64*(seg_id-1)):
			    user.readline()
			kkk = 73 if seg_id == 28 else 65
				
			for i in range(1, kkk, 1):
			    line = user.readline().strip().split(',')
			    yaw = float(line[7])
			    pitch = float(line[8])
			    roll = float(line[9])
			    pickle_path = "./pickles/fov_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode+'_'+ str(i)+".pkl"
                            if (os.path.isfile(pickle_path)):
                                viewed_fov = cPickle.load(open(pickle_path, "rb"))
                            else:
			        viewed_fov = viewport.ori_2_viewport(yaw, pitch, self.fov_degree_w, self.fov_degree_h, self.tile_w, self.tile_h)
			        cPickle.dump( viewed_fov, open(pickle_path, "wb"))
			    viewport.render_fov_local( VIDEO, user_id, seg_id, i, bitrate, viewed_fov)
			# concatenate all the frame into one video
			viewport.concat_image_2_video( VIDEO, user_id, seg_id, bitrate)
			user.close()
			expe = cv2.VideoCapture(repo+the_file)
			cont = cv2.VideoCapture("./360videos_60s/"+VIDEO+"_equir.mp4")
			frame_no = (seg_id - 1)*64 + 1
			for i in range(frame_no-1):
			    ret, imgC = cont.read()
			while(True):
			    ret, imgE = expe.read()
			    if(imgE is None):
				print >> sys.stderr, "next clip..."
				break
			    ret, imgC = cont.read()
			    if(imgC is None):
				print >> sys.stderr, "Error occured. Cannot read the video."
				break
			    tmp = frame_no%64 if frame_no%64!=0 else 64
			    pickle_path = "./pickles/fov_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode+'_'+str(tmp)+".pkl"
			    viewed_fov = cPickle.load(open(pickle_path,"rb"))
			    psnr = VPsnrCalc.VPsnrCalc(imgE, imgC, viewed_fov)
			    psnr_list.append(psnr)
			    print(str(frame_no)+" viewport_psnr:        "+str(psnr))
			    #filemanager.make_sure_path_exists("./PSNR")
			    f = open(psnr_name, "a")
			    f.write(str(frame_no).ljust(15)+',')
			    f.write(str(psnr).rjust(15))
			    f.write('\n')
			    f.close()
			    frame_no += 1
			for i in range(1, kkk):
			    pkk = "./pickles/fov_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode+'_'+str(i)+".pkl"
			    os.remove(pkk)
			shutil.rmtree("./tmp_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode)
			shutil.rmtree("./frame_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode)
		        f = open(psnr_name, "a")
			f.write("avg_psnr, ")
			f.write(str(sum(psnr_list)/len(psnr_list)))
			f.write('\n')
			f.close()
		    elif mode == "CR":
			tiled.mixed_tiles_quality(self.NO_OF_TILES, self.SEG_LENGTH, user_id, seg_id, VIDEO, bitrate, mode, [], viewed_tiles, [])
		    else:
			print >> sys.stderr, 'GGGGGGGGGGGGG'
			exit(0)

		    # sending ERP mp4 format video back to client
		    print >> sys.stderr, '\nsending video back to the client'
		    path_of_video = repo + the_file
		    video = open(path_of_video).read() 
		    video_size = os.path.getsize(path_of_video)
		    connection.sendall(video)
		    clientrecvts = time.time()
		    # seperate video into small chunks then transmit each of them
		    #count = 0
		    #while count < len(video):
		    #    chunk = video[count:count+self.CHUNK_SIZE]
		    #    connection.sendall(chunk)
		    #    count += self.CHUNK_SIZE
		    print >> sys.stderr, 'finished sending video\n'
		    connection.close()

		    # cloud server info
		    log_path = "./log/LOG_"+VIDEO+'_user'+user_id+'_'+str(seg_id)+'_'+bitrate+'_'+mode+".csv"
		    f = open( log_path, "a")
		    f.write(str(self.ENCODING_SERVER_ADDR) + ",")
		    f.write(str(self.ENCODING_SERVER_PORT) + ",")

		    # edge server info
		    f.write(str(self.EDGE_SERVER_ADDR) + ",")
		    f.write(str(self.EDGE_SERVER_PORT) + ",")
		
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
		    f.close()
		    
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

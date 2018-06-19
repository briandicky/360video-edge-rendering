#!/usr/bin/env python
#   Program:
#      To set up its socket differently from the way a server does. Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address. 
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.11
import threading
import socket 
import sys 
import time
import struct
import errno
import csv
from socket import error as SocketError


# Constants

CHUNK_SIZE = 4096




def client( server_addr, port, video, user_id, seg_id, mode, bitrate, repo):
        
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (server_addr, port)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        # Send data
        orientation = video+'_user'+str(user_id).zfill(2)+"_orientation.csv"
        user_data = []
        f = open("./360dataset/sensory/orientation/"+orientation, 'r')
        for row in csv.reader(f):
                user_data.append(row)
        user_data.pop(0)
        yaw = user_data[(seg_id-1)*64][-3]
        pitch = user_data[(seg_id-1)*64][-2]
        roll = user_data[(seg_id-1)*64][-1]
        ori = (format(time.time(), '.6f'), seg_id, yaw, pitch, roll, video, str(user_id).zfill(2), mode, bitrate)
        print >> sys.stderr, 'sending (%s, %s, %s, %s, %s, %s, %s %s %s)' % ori
        mes = str(ori[0]) + "," + str(ori[1]) + "," + str(ori[2]) + "," + str(ori[3]) + "," + str(ori[4]) + "," + str(ori[5]) + "," + str(ori[6]) + ',' + str(ori[7]) + ',' + str(ori[8])
        sock.sendall(mes)
        # Receive video from server
        filename = repo+video+'_user'+str(user_id).zfill(2)+'_'+str(seg_id).zfill(2)+'_'+bitrate+'_'+mode+".mp4"
        recvfile = open(filename, "w")
        print >> sys.stderr, 'downloading file...'
        # recv chunks from server then save all of them
        data = ""
        while True:
            chunk = sock.recv(CHUNK_SIZE)
            data += chunk
            if not chunk: break 
        recvfile.write(data)
        recvfile.close()
        print >> sys.stderr, 'finished downloading file'
    except SocketError:
        print("SocketError")
        # do somthing here
    finally:
        print >> sys.stderr, 'closing socket'
        sock.close()

#!/usr/bin/env python
#   Program:
#      To set up its socket differently from the way a server does. Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address. 
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.11

import socket 
import sys 
import time

# Constants
SERVER_ADDR = "140.114.77.125"
SERVER_PORT = 9487

CHUNK_SIZE = 4096

segid = 3
yaw = 3.03605833333
pitch = 0.103563888889
roll = -3.993
# End of constants

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    # Send data
    ori = (time.time(), segid, yaw, pitch, roll)
    print >> sys.stderr, 'sending (%s, %s, %s, %s, %s)' % ori
    mes = str(ori[0]) + "," + str(ori[1]) + "," + str(ori[2]) + "," + str(ori[3]) + "," + str(ori[4])
    sock.sendall(mes)

    # Receive video from server and save it
    filename = "output_" + str(ori[1]) + ".mp4"
    recvfile = open(filename, "w")
    print >> sys.stderr, 'writing file...'
    data = b''
    while True:
        tmp = sock.recv(CHUNK_SIZE)
        data += tmp
        if len(tmp) < CHUNK_SIZE: break
    
    recvfile.write(data)
    recvfile.close()
    print >> sys.stderr, 'finished writing file'

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

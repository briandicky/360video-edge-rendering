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

yaw = 30.0000583333
pitch = 3.24956388889
roll = -21.4974361111
# End of constants

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    # Send data
    ori = (time.time(), yaw, pitch, roll)
    print >> sys.stderr, 'sending (%s, %s, %s, %s)' % ori
    mes = str(ori[0]) + "," + str(ori[1]) + "," + str(ori[2]) + "," + str(ori[3])
    sock.sendall(mes)

    # Look for the response
    amount_received = 0
    amount_expected = len(mes)

    while amount_received < amount_expected:
        data = sock.recv(CHUNK_SIZE)
        amount_received += len(data)
        print >> sys.stderr, 'received "%s"' % data

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

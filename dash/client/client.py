#!/usr/bin/env python
#   Program:
#      To set up its socket differently from the way a server does. Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address. 
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.11

import socket 
import sys 

SERVER_ADDR = "140.114.77.125"
SERVER_PORT = 9487

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    # Send data
    message= 'This is the message.  It will be repeated.'
    print >> sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >> sys.stderr, 'received "%s"' % data

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

#!/usr/bin/env python
#   Program:
#       A server listens for incoming messages, or connect to other applications as a client.
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

# Bind the socket to the port
server_address = (SERVER_ADDR, SERVER_PORT)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection 
    print >> sys.stderr, 'waiting for a connection' 
    connection, client_address = sock.accept()

try:
    print >>sys.stderr, 'connection from', client_address

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        print >>sys.stderr, 'received "%s"' % data
        
        if data:
            print >>sys.stderr, 'sending data back to the client'
            connection.sendall(data)
        else:
            print >>sys.stderr, 'no more data from', client_address
            break

finally:
    # Clean up the connection
    connection.close()


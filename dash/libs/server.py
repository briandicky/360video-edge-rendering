#!/usr/bin/env python
#   Program:
#       A server listens for incoming messages, or connect to other applications as a client.
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

f = open("record.csv", "w")
f.write("serverip,serverport,serverts,clientip,clientport,clientts,rawYaw,rawPitch,rawRoll\n")
# End of constants

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
                f.write(str(SERVER_ADDR) + ",")
                f.write(str(SERVER_PORT) + ",")
                ts = time.time()
                f.write(str(ts) + ",")
                f.write(str(client_address[0]) + "," + str(client_address[1]) + ",")
                f.write(data)
                print >> sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >> sys.stderr, 'no more data from', client_address
                break
    finally:
        # Clean up the connection
        connection.close()


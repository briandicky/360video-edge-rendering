# 360 video edge rendering
This repository contains the source code to manipulate edge-assisted 360-degree videos streaming. 
In particular to prepare videos and run experiments for our proposals and papers. 


### Prerequisites
- Python2.7
- FFmpeg
- MP4Box
- OpenCV
- Cython

This software was only tested on linux (Ubuntu16.04).


### How to compile .pyx using cython and gcc, then create shared library
```
cython xxx.pyx
gcc -c -O3 -fPIC -I/usr/include/python2.7 xxx.c
gcc -shared xxx.o -o xxx.so
```

## Usage
### Run the server
```
python2.7 server.py

#No. of tiles = 3 x 3 = 9
#FoV width = 100, FoV height = 100
#Segment length = 4 sec

#starting up on 140.114.77.125 port 9487
#waiting for a connection...
```

### Run the client
```
cd client/
python2.7 client.py

#connecting to 140.114.77.125 port 9487
#sending (1524378869.771, 3, -120.036058333, 0.103563888889, -3.993)
```

### Switch the rendering mode
```
vim server.py

# viewing constants
class RENDER(Enum):
    CR = 1
    TR = 2
    VPR = 3
    TR_only = 4

# set rendering mode here
MODE = RENDER.TR
```

### Check the logs
```
vim log.csv

#edgeip,edgeport,clientip,clientport,segid,rawYaw,rawPitch,rawRoll,clienreqts,edgereqts,edgerecvts,clientrecvts
#140.114.77.125,9487,140.114.77.125,36420,3,-120.036058333,0.103563888889,-3.993,1524380472.727,1524380478.625,1524380478.931,1524380479.038
#140.114.77.125,9487,140.114.77.125,36444,3,-120.036058333,0.103563888889,-3.993,1524380480.324,1524380486.213,1524380486.519,1524380486.635
```

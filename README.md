# edge_rendering

### How to compile .pyx using cython and gcc, then create shared library
```
cython xxx.pyx
gcc -c -O3 -fPIC -I/usr/include/python2.7 xxx.c
gcc -shared xxx.o -o xxx.so
```

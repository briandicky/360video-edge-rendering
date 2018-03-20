# edge_rendering

### Using cython to compile .pyx, compile it using gcc, and create shared library

```
cython xxx.pyx
gcc -c -O3 -fPIC -I/usr/include/python2.7 xxx.c
gcc -shared xxx.o -o xxx.so
```

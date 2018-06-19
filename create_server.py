from server import *
import threading
from multiprocessing import Process

START_PORT = 30005

def main():
	#mode: 1=CR 2=TR 4=VPR
        SERVER_NUM = 10
	for i in range(SERVER_NUM):
		p = Server("140.114.89.208", START_PORT + i)
		p.start()
	for i in range(SERVER_NUM):
		p.join()

if __name__ == "__main__":
	main()

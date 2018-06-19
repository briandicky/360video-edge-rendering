from client import client
import threading
import time

#server_ip
#port
#user_id
#seg_id
#repo


class client_thread(threading.Thread):
    def __init__(self,  server_addr, port, video, mode, bitrate,repo, user_id):

        threading.Thread.__init__(self)
        self.server_addr = server_addr
        self.port = port
        self.video = video
        self.repo = repo
        self.mode = mode
        self.bitrate = bitrate
        self.user_id = user_id
    def run(self):
        for j in range(1,29):
            client(self.server_addr, self.port, self.video, self.user_id, j, self.mode, self.bitrate, self.repo)


th1 = client_thread("140.114.89.208", 20000, "game", "VPR", "1Mbps","./game/1Mbps/VPR/", 1)
th1.start()

th1 = client_thread("140.114.89.208", 20001, "game", "VPR", "2Mbps","./game/2Mbps/VPR/", 1)
th1.start()

th1 = client_thread("140.114.89.208", 20002, "game", "VPR", "4Mbps","./game/4Mbps/VPR/", 1)
th1.start()

th1 = client_thread("140.114.89.208", 20003, "game", "VPR", "8Mbps","./game/8Mbps/VPR/", 1)
th1.start()

th1 = client_thread("140.114.89.208", 20004, "game", "VPR", "16Mbps","./game/16Mbps/VPR/", 1)
th1.start()

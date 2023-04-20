import socket
import argparse
import threading
import sys
import hashlib
import time
import logging
import random

ip_address = 'localhost'
local_files = []
requesting = False
#TODO: Implement P2PClient that connects to P2PTracker
tracker = None #P2PTracker
transfer = None #transfer socket other clients connect to
conn = None #requesting clent

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

current_chunks = []
needed_chunks = []
num_needed = 0

def hashLocalFile(args, filename):
    index = filename[0]
    filename = filename[1]
    h = hashlib.sha1()
    filename = args.folder + "/" + filename
    with open(filename,'rb') as file:
        chunk = 0
        data = []
        while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           data.append(chunk)
           h.update(chunk)
        local_files.append((index,filename,data))
    return h.hexdigest()

def communicateTracker(conn, args):
    time.sleep(8)
    conn.send("WHERE_CHUNK,2".encode())
    time.sleep(1)
    print(conn.recv(1024).decode())
    while True:
        for i in current_chunks:
            if i in needed_chunks:
                needed_chunks.remove(i)

        idx = 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=int)
    parser.add_argument('-name', required=True)
    args = parser.parse_args()

    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(('localhost', 5100))

    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #clients connect to this
    transfer.bind(('localhost', args.transfer_port))
    #Step 0: send client name
    #Step 1: open localchunks.txt and figure out what files client has initially, then hash and send to tracker
    localchunks = "{}/local_chunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        chunk[1] = chunk[1].strip()
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(args, chunk)
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, ip_address, args.transfer_port)
            current_chunks.append(int(chunk[0]))

            tracker.send(chunkInfo.encode())
            time.sleep(1)

            chunk = lclchnks.readline().split(",")
            chunk[1] = chunk[1].strip()

            if chunk[1] == "LASTCHUNK":
                num_needed = int(chunk[0])
                chunks_needed = [range(1,num_needed + 1)]

        s = threading.Thread(target=communicateTracker, args=(tracker,args))
        s.start()
if __name__ == "__main__":
	main()
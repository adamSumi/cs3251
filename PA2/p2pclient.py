import socket
import argparse
import threading
import sys
import hashlib
import time
import logging


#TODO: Implement P2PClient that connects to P2PTracker

def hashLocalFile(filename):
    h = hashlib.sha1()
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
    return h.hexdigest()

def readChunks(args):
    localchunks = "{}/localchunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(chunk[1])
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, 'localhost', str(args.transfer_port))
            chunk = lclchnks.readline().split(",")

def collectChunk(idx, hash, ip1, port1, ip2, port2):
    pass

def sendChunk(idx, hash, ip1, port1, ip2, port2):
    pass

def recvTracker():
    pass

#WHERE_CHUNK -> COLLECT_CHUNK
def whereChunk(tracker,idx):
    tracker.send("WHERE_CHUNK,{}".format(idx).encode())
    find = tracker.recv(1024).decode()
    while find == "CHUNK_LOCATION_UNKNOWN,{}".format(idx):
        tracker.send("WHERE_CHUNK,{}".format(idx).encode())
        find = tracker.recv(1024).decode()

    dstInfo = find.split(",")
    collectChunk(int(dstInfo[1]),dstInfo[2], dstInfo[3], int(dstInfo[4]), dstInfo[5], int(dstInfo[6]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=str)
    parser.add_argument('-name', required=True)
    args = parser.parse_args()

    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(('localhost', 5100))

    #Step 1: open localchunks.txt and figure out what files client has initially, then hash and send to tracker
    localchunks = "{}/localchunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(chunk[1])
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, 'localhost', str(args.transfer_port))
            #SEND chunk to tracker here
            chunk = lclchnks.readline().split(",")





if __name__ == "__main__":
	main()
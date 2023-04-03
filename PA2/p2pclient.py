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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=str)
    parser.add_argument('-name', required=True)
    args = parser.parse_args()

    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(('localhost', 5100))

    #Step 1: open localchunks.txt and figure out what files client has, then hash and send to tracker
    localchunks = "{}/localchunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(chunk[1])
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, 'localhost', str(args.transfer_port))
            chunk = lclchnks.readline().split(",")



if __name__ == "__main__":
	main()
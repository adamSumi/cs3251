import socket
import argparse
import threading
import sys
import hashlib
import time
import logging

ip_address = 'localhost'
local_files = []
requesting = False
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

def readChunks(args): #in case we ever need to call it again after initialization?
    localchunks = "{}/localchunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(chunk[1])
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, 'localhost', str(args.transfer_port))
            chunk = lclchnks.readline().split(",")

def recvTracker(connection, args):
    while True:
        if not requesting:
            data = connection.recv(1024).decode()

#WHERE_CHUNK -> COLLECT_CHUNK
def whereChunk(tracker,idx):
    tracker.send("WHERE_CHUNK,{}".format(idx).encode())
    find = tracker.recv(1024).decode()
    while find.split(',')[0] == "CHUNK_LOCATION_UNKNOWN":
        tracker.send("WHERE_CHUNK,{}".format(idx).encode())
        find = tracker.recv(1024).decode()

    dstInfo = find.split(",")
    return(dstInfo)

def connectToClient(info):
    pass

def sendTracker(connection,args): #asks for chunk, looks for chunks, then automatically begins file transfer
    while True:
        try:
            message = input("")
            if message.split(",")[0] == "WHERE_CHUNK": #initial ask of where_chunk, if it can't find it whereChunk asks again automatically
                requesting = True
                chunkLocation = whereChunk(connection, message.split(',')[1])
                #connection.send("REQUEST_CHUNK,{}".format(message.split(',')[1]).encode())
                #source = connection.recv(1024).decode()
                connectToClient(chunkLocation)
                requesting = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=str)
    parser.add_argument('-name', required=True)
    args = parser.parse_args()

    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(('localhost', 5100))
    #Step 0: send client name
    tracker.send("{}".format(args.name).encode())
    #Step 1: open localchunks.txt and figure out what files client has initially, then hash and send to tracker
    localchunks = "{}/localchunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(chunk[1])
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, ip_address, str(args.transfer_port))
            local_files.append(chunkInfo)
            #SEND chunk to tracker here
            tracker.send(chunkInfo.encode())

            chunk = lclchnks.readline().split(",")

    s = threading.Thread(target=sendTracker, args=(tracker,args))
    s.start()




if __name__ == "__main__":
	main()
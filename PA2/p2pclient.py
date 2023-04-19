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

def monitorClientRequests(transfer):
    transfer.listen()
    while True:
        connection, address = transfer.accept()
        conn = connection

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
            local_files.append(chunkInfo)
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

    #dstInfo = find.split(",")
    return(find)

def connectToClient(info):
    #info recieved as: GET_CHUNK_FROM,<chunk_index>,<file_hash>,<IP_address1>,<Port_number1>,<IP_address2>,<Port_number2>,...
    info = info.split(",")
    chunk = info[1]
    fHash = info[2]
    clients = [(info[k],int(info[k+1])) for k in range(3,len(info),2)]
    grabClient = random.choice(clients)
    req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req.connect((grabClient[0], grabClient[1]))
    req.send("REQUEST_CHUNK,{}".format(chunk))
    # grab all the data that req sends back until we're out and req closes the connection on their side


def sendTracker(connection,args): #asks for chunk, looks for chunks, then automatically begins file transfer
    while True:
        try:
            message = input("")
            if message.split(",")[0] == "WHERE_CHUNK": #initial ask of where_chunk, if it can't find it whereChunk asks again automatically
                requesting = True
                chunkLocations = whereChunk(connection, message.split(',')[1])
                requesting = False
                return chunkLocations
                #connectToClient(chunkLocation)
            if message.split(",")[0] == "REQUEST_CHUNK":
                requesting = True
                chunkLocationsToSend = whereChunk(connection, message.split(',')[1])
                connectToClient(chunkLocationsToSend)
        except: break


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

            #after updating the list, we need to ask for other file chunks
            # sendTracker(connection, args) or something

    s = threading.Thread(target=sendTracker, args=(tracker,args))
    s.start()




if __name__ == "__main__":
	main()
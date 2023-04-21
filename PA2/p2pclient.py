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
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

current_chunks = []
needed_chunks = []
num_needed = 0

def debugThread():
    while True:
        for file in local_files:
            print(file[0])
        print("---------")
        time.sleep(3)

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
        local_files.append((int(index),filename,data))
    return h.hexdigest()

def hashFileFromList(info):
    h = hashlib.sha1()
    chunk = 0
    data = []
    for line in info:
        h.update(line)
    return h.hexdigest()

def sendChunk(sock):
    while True:
        connection, address = sock.accept()

        chunk_idx = int(connection.recv(1024).decode().split(",")[1])
        search_file = None
        for file in local_files:
            if file[0] == chunk_idx:
                search_file = file
                break

        connection.send(search_file[1].encode())

        for batch in search_file[2]:
            connection.send(batch)

        connection.close()

def handleTracker(conn, args):
    #time.sleep(8)
    #conn.send("WHERE_CHUNK,2".encode())
    #time.sleep(1)
    #print(conn.recv(1024).decode())
    while True:
        for i in current_chunks:
            if i in needed_chunks:
                needed_chunks.remove(i)

        idx = 0
        while len(needed_chunks) > 0:
            idx = idx % len(needed_chunks)
            search_idx = needed_chunks[idx]
            conn.send("WHERE_CHUNK,{}".format(search_idx).encode())
            time.sleep(1)
            logger.debug("{},WHERE_CHUNK,{}".format(args.name, search_idx))

            result = conn.recv(1024).decode() #As either CHUNK_LOCATION_UNKNOWN,<> || GET_CHUNK_FROM,<>,<>,{ip},{port},{ip},{port}...
            print(result)
            if result.split(",")[0] == "CHUNK_LOCATION_UNKNOWN":
                idx += 1
                continue
            else:
                header = result.split(",")[0:3] # GET_CHUNK_FROM,{search_idx},{file_hash}
                result = result.split(",")[3:]
                vendors = [(result[i],int(result[i+1])) for i in range(0, len(result)-1, 2)]
                chosen_vendor = random.choice(vendors)

                file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                file_socket.connect(chosen_vendor)

                file_socket.send("REQUEST_CHUNK,{}".format(search_idx))
                logger.debug("{},REQUEST_CHUNK,{},{},{}".format(args.name, search_idx, chosen_vendor[0],chosen_vendor[1]))

                file_name = file_socket.recv(1024).decode()
                #print(file_name)
                data = []
                while True:
                    packet = file_socket.recv(1024)
                    if not packet:
                        break
                    data.append(packet)

                newFileHash = hashFileFromList(data)
                local_files.append((search_idx, file_name, data))
                current_chunks.append(search_idx)
                chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(search_idx, newFileHash, ip_address, args.transfer_port)
                logger.debug("{},{}".format(args.name, chunkInfo))




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=int)
    parser.add_argument('-name', required=True)
    args = parser.parse_args()

    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(('localhost', 5100))

    debug = threading.Thread(target = debugThread, args = ())
    #debug.start()
    localchunks = "{}/local_chunks.txt".format(args.folder)
    with open(localchunks) as lclchnks:
        chunk = lclchnks.readline().split(",")
        chunk[1] = chunk[1].strip()
        while chunk[1] != 'LASTCHUNK':
            hashName = hashLocalFile(args, chunk)
            chunkInfo = "LOCAL_CHUNKS,{},{},{},{}".format(chunk[0], hashName, ip_address, args.transfer_port)
            logger.debug("{},{}".format(args.name, chunkInfo))
            current_chunks.append(int(chunk[0]))
            #print(chunkInfo)
            tracker.send(chunkInfo.encode())
            time.sleep(1)

            chunk = lclchnks.readline().split(",")
            chunk[1] = chunk[1].strip()

            if chunk[1] == "LASTCHUNK":
                num_needed = int(chunk[0])
                chunks_needed = [range(1,num_needed + 1)]

        s = threading.Thread(target=handleTracker, args=(tracker,args))
        s.start()

        transfer = socket.socket()
        transfer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transfer.bind((ip_address,args.transfer_port))
        transfer.listen(1)
        sc =threading.Thread(target=sendChunk(transfer))
        sc.start()
if __name__ == "__main__":
	main()


#LOG MESSAGE FORMATS
#<client_name>,LOCAL_CHUNKS,<chunk_index>,<file_hash>,<IP_address>,<Port_number>
#<client_name>,WHERE_CHUNK,<chunk_index>
#<client_name>,REQUEST_CHUNK,<chunk_index>,<IP_address>,<Port_number>
import socket
import argparse
import threading
import sys
import hashlib
import time
import logging

connections = {}
check_list = []
chunk_list = []

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def debugThread():
    while True:
        print(check_list)
        print("----")
        print(chunk_list)
        print("----------")
        time.sleep(5)

#data tuple list entry: ({chunk_index},{file_hash},{ip_addr},{transfer_port})
def manageLists():
    while True:
        for item in check_list:
            for otherItem in check_list:
                if item not in chunk_list and item != otherItem and item[0] == otherItem[0] and item[1] == otherItem[1]:
                    chunk_list.append(item)
                    chunk_list.append(otherItem)
                    check_list.remove(item)
                    check_list.remove(otherItem)

            for chunkItem in chunk_list:
                if item not in chunk_list and item != chunkItem and item[0] == chunkItem[0] and item[1] == chunkItem[1]:
                    chunk_list.append(item)
                    check_list.remove(item)

def findChunk(conn, chunk_idx, chunk_list):
    string = "GET_CHUNK_FROM,{}".format(chunk_idx)
    found = False
    for chunk in chunk_list:
        if chunk[0] == chunk_idx:
            if not found:
                string+=",{}".format(chunk[1])
            found = True
            ip_address, transfer_port = chunk[2], chunk[3]
            string += ",{},{}".format(ip_address, transfer_port)

    if not found:
        conn.send("CHUNK_LOCATION_UNKNOWN,{}".format(chunk_idx).encode())
        #print("bad")
        logger.debug("P2PTracker,CHUNK_LOCATION_UNKNOWN,{}".format(chunk_idx))
    else:
        conn.send(string.encode())
        #print(string)
        logger.debug("P2PTracker,{}".format(string))


def runTracker(conn):
    #username = conn.recv(1024).decode()
    #connections[username] = conn
    #print("new")
    while True:
        data = conn.recv(1024).decode()
        split_data = data.split(",")
        #print(split_data)
        if split_data[0] == "LOCAL_CHUNKS":
            dataTuple = (int(split_data[1]), split_data[2], split_data[3], int(split_data[4])) #LOCAL_CHUNKS,{chunk_index},{file_hash},{ip_addr},{transfer_port}
            check_list.append(dataTuple)
        if split_data[0] == "WHERE_CHUNK":
            findChunk(conn, int(split_data[1]), chunk_list)
def main():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5100))

    check_list = []
    chunk_list = []
    #print("Server started on localhost, port 5100. Accepting connections")
    #sys.stdout.flush()
    sock.listen(15) #15 is arbitrary value


    debug = threading.Thread(target = debugThread, args = ())
    #debug.start()
    cl = threading.Thread(target = manageLists, args=())
    cl.start()
    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=lambda: runTracker(connection))
        t.start()

    sock.close()

if __name__ == "__main__":
	main()
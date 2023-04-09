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

#TODO: Implement P2PTracker
#"LOCAL_CHUNKS,{chunk_index},{file_hash},{ip_addr},{transfer_port}"
def findFiles(info): #returns list of IPs and transfer ports
    pass
def checkHash(c1, c2):
    if c1[2] == c2[2]:
        return True
    return False
def checkSameFile():
    while True:
        for item in check_list:
            if any(item[1] == chunk_item[1] for chunk_item in chunk_list):
                chunk_list.append(item)
                check_list.remove(item)
            elif any(item[1] == check_item[1] for check_item in check_list if check_item != item):
                chunk_list.append(item)
                check_list.remove(item)
    #check_hashes = [k[1] for k in check_list]
    #for i in range(len(check_list)):
    #    check_chunk = check_list[i]
    #
    #    for j in range(len(check_list)):
    #        compChunk = check_list[j]
    #        #checks that we're not removing the comparison value, it's the same chunk, and it's the same file
    #        if (not j == i) and checkHash(check_chunk, compChunk):
    #            chunk_list.append(check_chunk)
    #            chunk_list.append(compChunk)
    #            check_list.remove(check_chunk)
    #            check_list.remove(compChunk)



def runTracker(connection):
    username = connection.recv(1024).decode()
    connections[username] = connection
    while True:
        data = connection.recv(1024).decode()
        if data.split(',')[0] == "LOCAL_CHUNKS":
            check_list.append(data.split(',')[1:])
        if data.split(',')[0] == "WHERE_CHUNK": #looks through CHUNKLIST for file and chunk idx, sends back GET_CHUNK_FROM
            res = findFiles(data.split(',')[1]) #passing in a string for the chunk ID, not integer


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5100))
    #print("Server started on localhost, port 5100. Accepting connections")
    #sys.stdout.flush()
    sock.listen(15) #25 is arbitrary value
    threads = []
    list_check = threading.Thread(target=checkSameFile, args=())
    list_check.start()

    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=runTracker, args=(connection))
        threads.append(t)
        t.start()

    sock.close()


if __name__ == "__main__":
	main()
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
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#TODO: Implement P2PTracker
#"LOCAL_CHUNKS,{chunk_index},{file_hash},{ip_addr},{transfer_port}"
#def findFiles(chunk_index): #returns list of IPs and transfer ports
def findFiles(chunk_index):
    chunk_list_ips = ["GET_CHUNK_FROM"]
    for item in chunk_list:
        item_index, item_hash, item_ip, item_port = item.split(',')
        if item_index == chunk_index:
            chunk_list_ips.append(f"{item_ip},{item_port}")

    if len(chunk_list_ips) == 1:
        return "CHUNK_UNAVAILABLE,{}".format(chunk_index)
    else:
        return ','.join(chunk_list_ips)

def checkHash(c1, c2):
    if c1[2] == c2[2]:
        return True
    return False
def checkSameFile():
    while True:
        for item in check_list:
            move = False
            tupleItem = item.split(",")
            for otherItem in check_list:
                if item != otherItem:
                    tOtherItem = otherItem.split(",")
                    if tupleItem[0] == tOtherItem[0] and checkHash(tupleItem[1],tOtherItem[1]):
                        move = True

            for otherItem in chunk_list:
                if item != otherItem:
                    tOtherItem = otherItem.split(",")
                    if tupleItem[0] == tOtherItem[0] and checkHash(tupleItem[1],tOtherItem[1]):
                        move = True

            if move:
                chunk_list.append(item)
                check_list.remove(item)
#------------------

        #first_index_set = set()
        #if chunk_list:
        #    first_index_set = {item.split(',')[0] for item in chunk_list}

        #check_list_pairs = []
        #for i in range(len(check_list)):
        #    for j in range(i + 1, len(check_list)):
        #        if check_list[i].split(',')[0] == check_list[j].split(',')[0]:
        #            check_list_pairs.append((check_list[i], check_list[j]))

        #for item in check_list:
        #    item_index, item_hash = item.split(',')[0], item.split(',')[1]
        #    if item_index in first_index_set and (not chunk_list or checkHash(item_hash, chunk_list[0].split(',')[1])):
        #        chunk_list.append(item)
        #    for pair in check_list_pairs:
        #        if item in pair and all(p in check_list for p in pair):
        #            pair_hashes = [p.split(',')[1] for p in pair]
        #            if all(checkHash(pair_hashes[0], h) for h in pair_hashes):
        #                chunk_list.extend(pair)
        #                for p in pair:
        #                    check_list.remove(p)

    #while True:
    #    for item in check_list:
    #        # is this supposed to check index or hash?
    #        if any(item[0] == chunk_item[0] for chunk_item in chunk_list):
    #            chunk_list.append(item)
    #            check_list.remove(item)
    #        elif any(item[0] == check_item[0] for check_item in check_list if check_item != item):
    #            chunk_list.append(item)
    #            check_list.remove(item)

def runTracker(connection):
    username = connection.recv(1024).decode()
    connections[username] = connection
    while True:
        data = connection.recv(1024).decode()
        split_data = data.split(",")
        if split_data[0] == "LOCAL_CHUNKS":
            #we might run into a problem with this using split instead of tuples to store in check_lis
            check_list.append(",".join(data.split(',')[1:]))

        if split_data[0] == "WHERE_CHUNK": #looks through CHUNKLIST for file and chunk idx, sends back GET_CHUNK_FROM
            req = findFiles(split_data[1]) #passing in a string for the chunk ID, not integer
            logger.info("P2PTracker,{}".format(req))
            connection.send(req.encode()) #check this line
            time.sleep(1)

def main():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5100))

    #print("Server started on localhost, port 5100. Accepting connections")
    #sys.stdout.flush()
    sock.listen(15) #25 is arbitrary value
    threads = []
    list_check = threading.Thread(target=checkSameFile, args=())
    list_check.start()

    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=lambda: runTracker(connection))
        threads.append(t)
        t.start()

    sock.close()


if __name__ == "__main__":
	main()
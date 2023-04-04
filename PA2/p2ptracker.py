import socket
import argparse
import threading
import sys
import hashlib
import time
import logging


#TODO: Implement P2PTracker
def runTracker(connection):
    while True:
        data = connection.recv(1024).decode()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5100))
    print("Server started on localhost, port 5100. Accepting connections")
    sys.stdout.flush()
    sock.listen(15) #25 is arbitrary value
    threads = []

    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=runTracker, args=(connection))
        threads.append(t)
        t.start()


if __name__ == "__main__":
	main()
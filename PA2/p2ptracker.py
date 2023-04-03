import socket
import argparse
import threading
import sys
import hashlib
import time
import logging


#TODO: Implement P2PTracker
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5100))
    print("Server started on localhost, port 5100. Accepting connections")
    sys.stdout.flush()
    sock.listen(15) #25 is arbitrary value

if __name__ == "__main__":
	main()
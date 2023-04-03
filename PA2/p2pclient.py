import socket
import argparse
import threading
import sys
import hashlib
import time
import logging


#TODO: Implement P2PClient that connects to P2PTracker
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder', required=True)
    parser.add_argument('-transfer_port', required=True,type=str)
    parser.add_argument('-name', required=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5100))

if __name__ == "__main__":
	main()
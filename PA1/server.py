import socket
import threading
import sys
import argparse

def main():
    #python3 server.py -start -port <port> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', nargs='?', const='', required=True)
    parser.add_argument('-port', required=True)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()
    print("Server started on port {}. Accepting connections".format(args.port))

if __name__ == "__main__":
	main()

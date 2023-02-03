import socket
import threading
import sys
import argparse


def clientCode(connection):
    pass
def main():
    #python3 server.py -start -port <port> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', nargs='?', const='', required=True)
    parser.add_argument('-port', required=True, type=str)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    host = '127.0.0.1'
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("Server started on port {}. Accepting connections".format(args.port))
    sock.listen(25) #25 is arbitrary value

    while True:
        connection, address = sock.accept()


if __name__ == "__main__":
	main()

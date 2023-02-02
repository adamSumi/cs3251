import socket
import threading
import sys
import argparse

def main():
    #python3 client.py -join -host <hostname> -port <port> -username <username> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', nargs='?', const='', required=True)
    parser.add_argument('-hostname', required=True)
    parser.add_argument('-port', required=True)
    parser.add_argument('-username', required=True)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    print('Connected to {} on port {}'.format(args.hostname, args.port))

if __name__ == "__main__":
	main()

#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents
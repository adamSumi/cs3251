import socket
import threading
import sys
import argparse

index = -1
def receiveThing(connection,args):
    while True:
        data = connection.recv(1024).decode().split(":")
        message = data[1:]
        cidx = int(data[0])

        if not cidx == index:
            print(message)
            sys.stdout.flush()

def sendThing(connection,args):
    while True:
        message = input("{0}: ".format(args.username))
        message = str(index) + ":" + message
        connection.send(message.encode())

def main():
    #python3 client.py -join -host <hostname> -port <port> -username <username> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', nargs='?', const='', required=True)
    parser.add_argument('-hostname', required=True,type=str)
    parser.add_argument('-port', required=True,type=int)
    parser.add_argument('-username', required=True)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.hostname, args.port))
    print('Connected to {} on port {}'.format(args.hostname, args.port))
    sys.stdout.flush()

    sock.send(args.passcode.encode())
    if sock.recv(1024).decode() == "bad":
        print('Password authentication failed.')
        sys.stdout.flush()
        sock.close()
    else:
        index = sock.recv(1024).decode()
        index = int(index)
        sock.send(args.username.encode())

        s = threading.Thread(target=sendThing, args=(sock,args))
        r = threading.Thread(target=receiveThing, args=(sock,args))
        s.start()
        r.start()



if __name__ == "__main__":
	main()

#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents
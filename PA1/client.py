import socket
import threading
import sys
import argparse

threads = []
#lock = threading.Lock()
def sendThing(connection,args):
    while True:
        try:
            message = input("")
            message = "{}: ".format(args.username) + message
            connection.send(message.encode())
            if message == ":Exit":
                break
        except:
            break

def receiveThing(connection,args):
    while True:
        try:
            message = connection.recv(1024).decode()
            if message == "server-quit":
                break
            print(message)
            sys.stdout.flush()
        except:
            break

def main():
    #python3 client.py -join -hostname <hostname> -port <port> -username <username> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', nargs='?', const='', required=True)
    parser.add_argument('-host', required=True,type=str)
    parser.add_argument('-port', required=True,type=int)
    parser.add_argument('-username', required=True)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    sock.send(args.passcode.encode())
    res = sock.recv(1024).decode()
    if res == "bad":
        print('Incorrect password')
        sys.stdout.flush()
    elif not res == "bad":
        print('Connected to {} on port {}'.format(args.host, args.port))
        sys.stdout.flush()
        sock.send(args.username.encode())

        s = threading.Thread(target=sendThing, args=(sock,args))
        r = threading.Thread(target=receiveThing, args=(sock,args))
        s.start()
        r.start()




if __name__ == "__main__":
	main()

#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents
import socket
import threading
import sys
import argparse

messages = []
threads = []
#brain dump for potential server code
def serverMsg(sock): #sends messages from other clients to everyone else
    while True:
        if len(messages) > 0:
            sock.send(messages[0].encode())
            messages.pop()

def clientCode(connection, ar, setup): # recieves messages from client, and checks for pass code
    pcode = connection.recv(1024).decode()
    if not pcode == ar.passcode:
        message = "bad"
        connection.send(message.encode())
        connection.close()
    else:
        message = "good"
        connection.send(message.encode())
        username = connection.recv(1024).decode()

    while True:
        message = connection.recv(1024).decode()
        print("{0}: {1}".format(username, message))
        sys.stdout.flush()

        messages.append(message)


def main():
    #python3 server.py -start -port <port> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', nargs='?', const='', required=True)
    parser.add_argument('-port', required=True, type=int)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    host = '127.0.0.1'
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("Server started on port {}. Accepting connections".format(args.port))
    sys.stdout.flush()
    sock.listen(15) #25 is arbitrary value

    s = threading.Thread(target=serverMsg, args=(sock, args))
    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=clientCode, args=(connection, args, False))
        threads.append(t)
        t.start()

    sock.close()



if __name__ == "__main__":
	main()

import socket
import threading
import sys
import argparse

messages = []
threads = []
#brain dump for potential server code
def serverMsg(sock): #sends messages from other clients to everyone else
    while len(messages) > 0:
        "{0} said: {1}"
        sock.send(messages[0])
        messages.pop()

def clientCode(connection, ar): # recieves messages from client, and checks for pass code
    pcode = connection.recv(1024)
    if not pcode == ar.passcode:

        connection.close()
    else:
        username = connection.recv(1024)
        while True:
            message = connection.recv(1024)
            print("{0}: {1}".format(username, message))
            sys.stdout.flush()

            messages.append(message)



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
    sys.stdout.flush()
    sock.listen(25) #25 is arbitrary value

    s = threading.Thread(target=serverMsg, args=(sock))

    while True:
        connection, address = sock.accept()
        t = threading.Thread(target=clientCode, args=(connection, args))
        threads.append(t)
        t.start()



if __name__ == "__main__":
	main()

import socket
import threading
import sys
import argparse

idx= 0
messages = []
threads = []
connections =[]
#brain dump for potential server code
def sendToClients(message,cid):
    print(cid)
    sys.stdout.flush()
    for con in connections:
        if cid not in con:
            con[0].send(message)
def serverMsg(sock): #sends messages from other clients to everyone else
    while True:
        if len(messages) > 0:
            sock[0].send(messages[0])
            sendToClients(messages[0])
            messages.pop()

def clientCode(connection, ar, idx): # recieves messages from client, and checks for pass code
    pcode = connection.recv(1024).decode()
    if not pcode == ar.passcode:
        connection.send("bad".encode())
        connection.close()
    else:
        #message = str(index)
        connection.send(str(idx).encode())
        username = connection.recv(1024).decode()
        messages.append("{} has joined the chatroom".format(username))

        while True:
            msg = connection.recv(1024).decode().split("|")
            ci = int(msg[0])
            message = "".join(msg[1:])
            print("{}".format(message))
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

    idx = 0
    s = threading.Thread(target=serverMsg, args=(sock, args))
    while True:
        connection, address = sock.accept()
        print("Something accepted")
        sys.stdout.flush()
        connections.append((connection,idx))
        t = threading.Thread(target=clientCode, args=(connection, args, idx), daemon=True)
        threads.append(t)
        t.start()
        idx+=1

    sock.close()



if __name__ == "__main__":
	main()

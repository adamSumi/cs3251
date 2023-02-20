import socket
import threading
import sys
import argparse

idx= 0
messages = [] #[idx, message w/ user]
usernames = []
threads = []
connections ={}
#brain dump for potential server code
def sendToClients(user, message):
    for client in connections:
        if not client == user:
            connections[client].send(message.encode())


def clientCode(connection, ar, idx): # recieves messages from client, and checks for pass code
    pcode = connection.recv(1024).decode()
    if not pcode == ar.passcode:
        connection.send("bad".encode())
    else:
        connection.send("good".encode())
        username = connection.recv(1024).decode()
        connections[username] = connection
        messages.append("{} has joined the chatroom".format(username))
        print("{} has joined the chatroom".format(username))
        sys.stdout.flush()

        sendToClients(username,"{} has joined the chatroom".format(username))

        while True: #messages should be recieved as "{username}: {message}"
            data = connection.recv(1024).decode().split(": ")
            user = data[0]
            msg = "".join(data[1:])
            if msg == ":Exit":
                connection.send("server-quit".encode())
                connections[user].close()
                del connections[user]
                print("{} has left the chat".format(user))
                sys.stdout.flush()
                sendToClients(user, "{} has left the chat".format(user))
                break
            else:
                print("{} says: {}".format(user, msg))
                sys.stdout.flush()
                sendToClients(user, "{} says: {}".format(user, msg))
            #print("{}".format(message)) #prints message server side

            #rint(msg)


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
    while True:
        connection, address = sock.accept()
        #print("Something accepted")
        #sys.stdout.flush()
        #connections.append((connection,idx))
        t = threading.Thread(target=clientCode, args=(connection, args, idx))
        threads.append(t)
        t.start()
        idx+=1

    sock.close()



if __name__ == "__main__":
	main()

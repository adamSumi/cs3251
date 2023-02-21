import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta

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
        messages.append("{} joined the chatroom".format(username))
        print("{} joined the chatroom".format(username))
        sys.stdout.flush()

        sendToClients(username,"{} joined the chatroom".format(username))

        while True: #messages should be recieved as "{username}: {message}"
            data = connection.recv(1024).decode().split(": ")
            user = data[0]
            msg = "".join(data[1:])
            if msg == ":Exit":
                connection.send("server-quit".encode())
                connections[user].close()
                del connections[user]
                print("{} left the chatroom".format(user))
                sys.stdout.flush()
                sendToClients(user, "{} left the chatroom".format(user))
                break
            elif msg == ":)":
                print("{}: [feeling happy]".format(user))
                sys.stdout.flush()
                sendToClients(user, "{}: [feeling happy]".format(user))
            elif msg == ":(":
                print("{}: [feeling sad]".format(user))
                sys.stdout.flush()
                sendToClients(user, "{}: [feeling sad]".format(user))
            elif msg == ":mytime":
                today = datetime.now()
                print("{}: {}".format(user, today.strftime("%c")))
                sys.stdout.flush()
                sendToClients(user, "{}: {}".format(user, today.strftime("%c")))
            elif msg == ":+1hr":
                plus_one = datetime.today()
                plus_one = plus_one + timedelta(hours=1)
                print("{}: {}".format(user, plus_one.strftime("%c")))
                sys.stdout.flush()
                sendToClients(user, "{}: {}".format(user, plus_one.strftime("%c")))
            elif msg[0] == "\\":
                print("{}: {}".format(user, msg[1:]))
                sys.stdout.flush()
                sendToClients(user, "{}: {}".format(user, msg[1:]))
            else:
                print("{}: {}".format(user, msg))
                sys.stdout.flush()
                sendToClients(user, "{}: {}".format(user, msg))
            #print("{}".format(message)) #prints message server side

            #rint(msg)


def main():
    #python3 server.py -start -port <port> -passcode <passcode>
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', nargs='?', const='', required=True)
    parser.add_argument('-port', required=True, type=int)
    parser.add_argument('-passcode', required=True)
    args = parser.parse_args()

    hostname = '127.0.0.1'
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((hostname, port))
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

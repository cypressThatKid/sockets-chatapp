import socket
import threading

host = '0.0.0.0' #host to listen on, should always be 0.0.0.0 unless you know what you're doing
port = 55555 #this can be changed, make sure to reflect your change in the config file

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() #start server

clients = []
nicknames = []

#broadcast message to everyone
def broadcast(message):
    for client in clients:
        client.send(message)

#handling messages
def handle(client):
    while True:
        try:
            #broadcasting messages that we recieve
            message = client.recv(1024)
            broadcast(message)
        except:
            #remove/closing clients connections when they leave/disconnect
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

#recieving and listening
def receive():
    while True:
        #accept client connection
        client, address = server.accept()
        print("Connected with {}".format(str(address))) #print ip

        #request nickname, store it in nicknames list
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        #announce the joining of the client
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        with open("motd.txt", "r") as f:
                motd = f.read()
        with open("banner.txt", "r") as ff:
            banner = ff.read()
        client.send(banner.encode('ascii'))
        client.send(motd.encode('ascii'))
        #threading
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

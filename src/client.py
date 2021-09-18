import socket
import threading
import os

#nickname prompt
nickname = input("Choose your nickname: ")

#connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.115', 55555))

def receive():
    while True:
        try:
            #sending nickname when the server requests us to
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

#sending messages to the server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

#listening thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#writing thread
write_thread = threading.Thread(target=write)
write_thread.start()



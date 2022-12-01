import socket
import threading
import os

client_socket = socket.socket()
client_socket.connect(('localhost', 12000))

def receive(client_socket):
    try:
        data = ""
        while data != "disconnect" and data != "kill":
            data = client_socket.recv(1024).decode()
            print(f"Message reçu du serveur : {data}")
        client_socket.close()
    except ConnectionAbortedError:
         print("Socket fermée")

t2 = threading.Thread(target=receive, args=[client_socket])
t2.start()


message = ""
while message != "disconnect" and message != "kill":
    message = input("Message à envoyer au Serveur : ")
    client_socket.send(message.encode())
client_socket.close()

t2.join()
client_socket.close()














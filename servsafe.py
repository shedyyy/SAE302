import socket
import threading
import os
import subprocess
import platform
import psutil


def commande(data):
    cmd = data.split(':')
    if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
        if cmd[1] == "dir":
            reply = subprocess.getoutput("dir")[228:]
            conn.send(reply.encode())
            print(f"Checkbug : DIR FAIT")
        elif cmd[1][:6] == "mkdir ":
            if len(cmd[1][6:]) != 0:
                dos =cmd[1][6:]
                reply = subprocess.getoutput(f"mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\{dos}")[228:]
                conn.send(reply.encode())
                print(f"Checkbug : MKDIR {dos} FAIT")
            else:
                print("Impossible de créer un dossier sans nom")
        else:
            print("Erreur : Commande Windows incomplète ou inconnue")
    elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
        if cmd[1] == "get-process":
            reply = subprocess.getoutput("powershell.exe get-process")[228:]
            conn.send(reply.encode())
            print(f"Checkbug : Powershell:get-process FAIT")
        else:
            print("Erreur : Commande Powershell inconnue")
    elif data == "Linux:ls -la":
        reply = subprocess.getoutput("ls -la")
        conn.send(reply.encode())
        print(f"Checkbug : ls -la FAIT")
    elif data == "python --version":
        reply = subprocess.getoutput("python --version")[228:]
        conn.send(reply.encode())
        print(f"Checkbug : python --version FAIT")
    elif data == "ping 192.168.152.1":
        reply = subprocess.getoutput("ping 192.168.152.1")[228:]
        conn.send(reply.encode())
        print(f"Checkbug : PING FAIT")
    elif data == "OS":
        reply = platform.platform()
        conn.send(reply.encode())
        print("OS renvoyé")
    elif data == "Name":
        reply = socket.gethostname()
        conn.send(reply.encode())
        print("Nom envoyé")
    elif data == "IP":
        hostname = socket.gethostname()
        reply = socket.gethostbyname(hostname)
        conn.send(reply.encode())
        print("IP envoyé")
    elif data == "CPU":
        reply = str(f"{psutil.cpu_percent()}% du CPU utilisé !")
        conn.send(reply.encode())
        print("Checkbug : Info CPU envoyée")
    elif data == "RAM":
        reply = str(f"{psutil.virtual_memory().percent}% de la RAM utilisé ! \nRAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
        conn.send(reply.encode())
        print("Checkbug : Info RAM envoyée")
    else:
        print(f"Message reçu du client : {data}")



server_socket = socket.socket()
server_socket.bind(('localhost', 12000))
reply = ""
data = ""
server_socket.listen(5)


try:
    while data != "kill":
            conn, address = server_socket.accept()
            reply = ""
            data = ""
            while data != "disconnect":
                data = conn.recv(1024).decode()
                commande(data)
            conn.close()
    server_socket.close()
except ConnectionResetError:
    print("")




def recept(conn):
    data=""
    try:
        while data != "disconnect":
            data = conn.recv(1024).decode()
            commande(data)
            print(data)
    except ConnectionResetError:
        print("Socket Fermée")


t2 = threading.Thread(target=recept, args=[conn])
t2.start()





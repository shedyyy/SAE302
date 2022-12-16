import socket
import subprocess
import platform
import psutil
import sys




def Server():
    data = ""
    while data != "kill" :
        data = ""
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 10000))
        server_socket.listen(10)

        print('Awaiting connection')
        while data != "kill" and data != "reset":
            data = ""
            try :
                conn, addr = server_socket.accept()
                print (addr)
            except ConnectionError:
                print ("Connection Error")
                break
            else :
                try:
                    while data != "kill" and data != "reset" and data != "disconnect":
                        data = conn.recv(1024).decode()
                        print ("Command used: ", data)
                        cmd = data.split(':')
                        cmdping = data.split(' ')
                        if cmd[0].lower() == "dos" and sys.platform == 'win32':
                            try:
                                reply = subprocess.check_output(cmd[1], shell=True).decode('cp850').strip()
                            except:
                                reply = "Unknown Windows command!"
                                conn.send(reply.encode())
                            else:
                                if reply == "":
                                    conn.send(reply.encode())
                                else:
                                    conn.send(reply.encode())
                        elif cmd[0].lower() == "powershell" and sys.platform == 'win32':
                            try:
                                reply = subprocess.check_output(f"powershell.exe {cmd[1]}", shell=True).decode('cp850').strip()
                            except:
                                reply = "Unknown Powershell command!"
                                conn.send(reply.encode())
                            else:
                                conn.send(reply.encode())

                        elif data.lower() == "python --version":
                             rep = str(subprocess.check_output('python --version', shell=True))
                             output = rep.replace('b', '').replace('\\r', "").replace('\\n', "")
                             conn.send(output.encode())
                             print("Succesfully sent the current Python version installed in the machine to the client")

                        elif cmdping[0].lower() == "ping" and len(cmdping[1]) !=0:
                             rep = subprocess.getoutput(data)
                             conn.send(rep.encode())
                             print(f"Succesfully pinged the IP")

                        elif data.lower() == "os":
                             rep = platform.platform()
                             conn.send(rep.encode())
                             print("Succesfully sent the machine's OS information to the client")

                        elif data.lower() == "name":
                             rep = socket.gethostname()
                             conn.send(rep.encode())
                             print("Succesfully sent the machine's hostname to the client")

                        elif data.lower() == "ip":
                             hostname = socket.gethostname()
                             rep = str(f"{socket.gethostbyname(hostname)}")
                             conn.send(rep.encode())
                             print("Succesfully sent the machine's IP to the client")

                        elif data.lower() == "cpu":
                             rep = str(f'{psutil.cpu_percent()}% of the CPU used.')
                             conn.send(rep.encode())
                             print("Succesfully sent the machine's CPU information to the client")

                        elif data.lower() == "ram":
                             rep = str(f'RAM used: {psutil.virtual_memory().percent}% \nTotal memory: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB \nMemory left: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB')
                             conn.send(rep.encode())
                             print("Succesfully sent the machine's RAM information to the client")

                        elif data == "kill" or data == "reset" or data == "disconnect":
                            conn.send(data.encode())
                        else:
                            reply = "Inexisting command! Please retry"
                            conn.send(reply.encode())
                except ConnectionResetError:
                    print("")
                except ConnectionAbortedError:
                    print("")
            conn.close()
        print ("Connection closed")
        server_socket.close()
        print ("Server closed")

if __name__ == '__main__':
    Server()

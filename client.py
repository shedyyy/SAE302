from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import socket, pathlib, sys

class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None

    
    def connection(self):
            self.__sock.connect((self.__host, self.__port))

    def connect(self):
        try :
            self.__sock.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            print ("Connection Refused Error")
            return -1
        except ConnectionError:
            print ("Connection Error")
            return -1
        else :
            print ("Connection succesful")
            return 0

    def communication(self, msg):
        self.__sock.send(msg.encode())
        reponse = self.__sock.recv(32000).decode()
        return reponse





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__host = QLabel("Host")
        self.__port = QLabel("Port")
        self.__newip = QLabel("New IP:")
        self.__addip = QPushButton("Add")
        self.__entercommand = QLabel("Command: ")
        self.__response = QLabel("Server response: ")
        self.__newiptext = QLineEdit("")
        self.__entertext = QTextEdit(self)
        self.__iptext = QComboBox()
        self.__porttext = QLineEdit("")
        self.__commandstext = QLineEdit("")
        self.__filetext = QLineEdit("")
        self.__savefile = QLineEdit("")
        self.__newiptext.hide()
        self.__newip.hide()
        self.__addip.hide()
        self.__savefile.hide()
        self.__addip.setEnabled(False)
        self.__w = None


        self.__client = None
        self.__connectbutton = QPushButton("Connect")
        self.__send = QPushButton("Send")
        self.__filename = QPushButton("Choose")


        self.__filetext.setReadOnly(True)
        self.__entertext.hide()
        self.__entercommand.hide()
        self.__commandstext.hide()
        self.__labnomfichier = QLabel("Source file:")
        grid.addWidget(self.__newip, 9, 0)
        grid.addWidget(self.__addip, 9, 2)
        grid.addWidget(self.__entertext, 3, 0, 1, 5)
        grid.addWidget(self.__host, 2, 0)
        grid.addWidget(self.__port, 3, 0)
        grid.addWidget(self.__entercommand, 2, 0)
        grid.addWidget(self.__response, 3, 0)
        grid.addWidget(self.__iptext, 2, 1)
        grid.addWidget(self.__porttext, 3, 1)
        grid.addWidget(self.__newiptext, 9, 1)
        self.__commandstext.setPlaceholderText("Enter your command here!")
        grid.addWidget(self.__commandstext, 2, 1, 1, 3)
        self.__porttext.setPlaceholderText("Enter the port used on the server file")
        self.__commandstext.setText("")
        self.__newiptext.setPlaceholderText("Enter a new IP here")
        self.__entertext.setReadOnly(True)
        grid.addWidget(self.__connectbutton, 4, 1)
        grid.addWidget(self.__send, 2, 4)
        grid.addWidget(self.__labnomfichier, 8, 0)
        grid.addWidget(self.__filetext, 8, 1)
        grid.addWidget(self.__filename, 8, 2)
        grid.addWidget(self.__savefile, 10, 2)



        self.__connectbutton.clicked.connect(self.connectbuttonnexion)
        self.__send.clicked.connect(self.command1)
        self.__addip.clicked.connect(self.ajout)
        self.__filename.clicked.connect(self.filename)
        self.__send.hide()
        self.__response.hide()
        self.__connectbutton.setEnabled(False)



        self.setWindowTitle("SAE3.02")


    def command1(self):
        msg = self.__commandstext.text()
        try:
            reponse = self.__client.communication(msg)
        except:
            self.__entertext.append(f"The server is off or you aren't connected anymore! Please verify your settings\n")
        else:
            self.__entertext.append(f"{reponse}\n")
            self.__commandstext.clear()





    def filename(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Choose your file", "", "Text files (*.txt)", options=options)
            testest = pathlib.Path(fileName).name
            self.__filetext.setText(fileName)
            file1 = open(f"{testest}", 'r')
            Lines = file1.readlines()
            count = 0
            for line in Lines:
                count += 1
                self.__iptext.addItem(line.strip())
            self.__connectbutton.setEnabled(True)
            self.__addip.setEnabled(True)
            self.__newiptext.show()
            self.__newip.show()
            self.__addip.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please choose a file before closing!!!")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()






    def connectbuttonnexion(self):
        try:
            host = str(self.__iptext.currentText())
            port = int(self.__porttext.text())
            self.__client = Client(host, port)
            self.__client.connection()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Connection is not possible! Make sure the server is ON or that you have entered the right IP.")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            self.__connectbutton.setEnabled(False)
            self.__send.show()
            self.__entertext.show()
            self.__entercommand.show()
            self.__commandstext.show()
            self.__porttext.hide()
            self.__host.hide()
            self.__addip.hide()
            self.__newip.hide()
            self.__port.hide()
            self.__porttext.hide()
            self.__newiptext.hide()
            self.__connectbutton.hide()
            self.__filetext.hide()
            self.__labnomfichier.hide()
            self.__filename.hide()

    def ajout(self):
        if self.__newiptext.iptext() != "":
            testest = self.__filetext.iptext()
            file = open(f"{testest}", "a")
            file.write(f"\n{self.__newiptext.text()}")
            self.__iptext.addItem(self.__newiptext.text())
            self.__newiptext.setText("")
            self.__savefile = self.__filetext.text()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Please add an IP")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    def _actionQuitter(self):
        QCoreApplication.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

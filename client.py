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

    def connect(self) -> int:
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

    def connection(self):
            self.__sock.connect((self.__host, self.__port))


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
        self.__lab = QLabel("Host")
        self.__lab8 = QLabel("Port")
        self.__labadd = QLabel("New IP:")
        self.__btnadd = QPushButton("Add")
        self.__lab5 = QLabel("Command: ")
        self.__lab9 = QLabel("Server response: ")
        self.__info = QLabel("Informations \n( Host / Port )")
        self.__lab2 = QLabel("")
        self.__text10 = QLineEdit("")
        self.__lab3 = QTextEdit(self)
        self.__lab4 = QLabel("")
        self.__labvide = QLabel("")
        self.__text = QComboBox()
        self.__text2 = QLineEdit("")
        self.__text3 = QLineEdit("")
        self.__text11 = QLineEdit("")
        self.__savefichier = QLineEdit("")
        self.__infohost = QLineEdit("")
        self.__infoport = QLineEdit("")
        self.__infoportlabel = QLabel("")
        self.__infohostlabel = QLabel("")
        self.__text10.hide()
        self.__labadd.hide()
        self.__btnadd.hide()
        self.__savefichier.hide()
        self.__btnadd.setEnabled(False)
        self.__w = None




        self.__client = None
        self.__okcon = QPushButton("Connect")
        self.__okcom = QPushButton("Send")
        self.__newconnection = QPushButton("New connection")
        self.__fichiername = QPushButton("Choose")


        self.shortcut_open = QShortcut(QKeySequence('Return'), self)
        self.shortcut_open.activated.connect(self.command1)
        self.shortcut_open2 = QShortcut(QKeySequence('Enter'), self)
        self.shortcut_open2.activated.connect(self.command1)


        # Using readlines()
        self.__text11.setReadOnly(True)
        self.__lab3.hide()
        self.__lab5.hide()
        self.__text3.hide()
        self.__labnomfichier = QLabel("Source file:")
        grid.addWidget(self.__info, 0, 0)
        grid.addWidget(self.__labadd, 9, 0)
        grid.addWidget(self.__labvide, 6, 0)
        grid.addWidget(self.__btnadd, 9, 2)
        grid.addWidget(self.__infohost, 0, 1)
        grid.addWidget(self.__infoport, 0, 2)
        grid.addWidget(self.__infoportlabel, 0, 2)
        grid.addWidget(self.__infohostlabel, 0, 1)
        grid.addWidget(self.__lab3, 3, 0, 1, 5)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(self.__lab4, 1, 1)
        grid.addWidget(self.__lab, 2, 0)
        grid.addWidget(self.__lab8, 3, 0)
        grid.addWidget(self.__lab5, 2, 0)
        grid.addWidget(self.__lab9, 3, 0)
        grid.addWidget(self.__text, 2, 1)
        grid.addWidget(self.__text2, 3, 1)
        grid.addWidget(self.__text10, 9, 1)
        self.__text3.setPlaceholderText("Enter your command here!")
        grid.addWidget(self.__text3, 2, 1, 1, 3)
        self.__text2.setText("10000")
        self.__text3.setText("")
        self.__text10.setPlaceholderText("Enter a new IP here")
        self.__lab3.setReadOnly(True)
        grid.addWidget(self.__okcon, 4, 1)
        grid.addWidget(self.__okcom, 2, 4)
        grid.addWidget(self.__newconnection, 0, 3)
        grid.addWidget(self.__labnomfichier, 8, 0)
        grid.addWidget(self.__text11, 8, 1)
        grid.addWidget(self.__fichiername, 8, 2)
        grid.addWidget(self.__savefichier, 10, 2)



        self.__info.hide()
        self.__infohost.hide()
        self.__infoport.hide()
        self.__infoportlabel.hide()
        self.__infohostlabel.hide()
        self.__newconnection.hide()
        self.__okcon.clicked.connect(self.okconnexion)
        self.__okcom.clicked.connect(self.command1)
        self.__newconnection.clicked.connect(self.newconnection)
        self.__btnadd.clicked.connect(self.ajout)
        self.__fichiername.clicked.connect(self.fichiernom)
        self.__okcom.hide()
        self.__lab9.hide()
        self.__okcon.setEnabled(False)



        self.setWindowTitle("SAE3.02")


    def command1(self):
        msg = self.__text3.text()
        try:
            reponse = self.__client.communication(msg)
        except:
            self.__lab3.append(f"The server is off or you aren't connected anymore! Please verify your settings\n")
        else:
            self.__lab3.append(f"{reponse}\n")
            self.__text3.clear()





    def fichiernom(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Choose your file", "", "Text files (*.txt)", options=options)
            testest = pathlib.Path(fileName).name
            self.__text11.setText(fileName)
            file1 = open(f"{testest}", 'r')
            Lines = file1.readlines()
            count = 0
            for line in Lines:
                count += 1
                self.__text.addItem(line.strip())
            self.__okcon.setEnabled(True)
            self.__btnadd.setEnabled(True)
            self.__text10.show()
            self.__labadd.show()
            self.__btnadd.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please choose a file before closing!!!")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()


    def newconnection(self):
        self.__w = MainWindow()
        self.__w.show()




    def okconnexion(self):
        try:
            host = str(self.__text.currentText())
            port = int(self.__text2.text())
            self.__client = Client(host, port)
            self.__client.connection()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Connection is not possible! Make sure the server is ON or that you have entered the right IP.")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            self.__okcon.setEnabled(False)
            self.__okcom.show()
            self.__lab3.show()
            self.__lab5.show()
            self.__infohost.show()
            self.__infoport.show()
            self.__infoport.setEnabled(False)
            self.__infohost.setEnabled(False)
            self.__infoportlabel.show()
            self.__infohostlabel.show()
            self.__text3.show()
            self.__text2.hide()
            self.__lab.hide()
            self.__btnadd.hide()
            self.__labadd.hide()
            self.__info.show()
            self.__lab8.hide()
            # self.__lab9.show()
            self.__text2.hide()
            self.__text10.hide()
            self.__okcon.hide()
            self.__newconnection.show()
            self.__text11.hide()
            self.__labnomfichier.hide()
            self.__fichiername.hide()
            self.__infoportlabel.setText(f" {self.__text2.text()}")
            self.__infohostlabel.setText(f" {self.__text.currentText()}")

    def ajout(self):
        if self.__text10.text() != "":
            testest = self.__text11.text()
            file = open(f"{testest}", "a")
            file.write(f"\n{self.__text10.text()}")
            self.__text.addItem(self.__text10.text())
            self.__text10.setText("")
            self.__savefichier = self.__text11.text()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Impossible d'ajouter un host vide")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()






    def _actionQuitter(self):
        QCoreApplication.exit(0)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

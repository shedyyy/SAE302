import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        lab = QLabel("Nom Machine")
        lab3 = QLabel("IP")
        lab4 = QLabel("Port")
        self.__lab2 = QLabel("")
        self.__text = QLineEdit("")
        self.__text2 = QLineEdit("")
        self.__text3 = QLineEdit("")
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")


        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(lab, 0, 0)
        grid.addWidget(lab4, 2, 0)
        grid.addWidget(lab3, 1, 0)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 1, 1)
        grid.addWidget(self.__text3, 2, 1)
        grid.addWidget(ok, 5, 1)
        grid.addWidget(quit, 5, 0)
        ok.clicked.connect(self._actionOk)
        quit.clicked.connect(self._actionQuitter)
        self.setWindowTitle("Application - Surveillance")

    def _actionOk(self):
        self.__lab2.setText(f"{self.__text.text()} {self.__text2.text()} {self.__text3.text()}")
        header = ['nom', 'ip', 'port']
        data = [f"{self.__text.text()}, {self.__text2.text()}, {self.__text3.text()}"]

        with open('MDR.csv', 'w', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write the data
            writer.writerow(data)


    def _actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()














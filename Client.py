import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QGridLayout, QLabel, QGroupBox
from PyQt5.QtGui import QPainter, QPixmap
from settings import pin_names, pins_to_control
from protocol import SetPin, Response, CheckPins, CheckPinsResponse

HOST = '192.168.0.103'
PORT = 8888

class Client(QDialog):
    def __init__(self):
        super().__init__()
        super().__init__()
        self.title = 'RaspberryPi Controll'
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 500
        self.initUI()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = CheckPins.get_binary()
            s.sendall(message)
            data = s.recv(1024)
        print('Received', repr(data))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(6, 1)

        pin_image_raw =  QPixmap('images/pin.png')
        pin_image_rotated_raw = QPixmap('images/pin_rotated.png')

        for i in range(40):
            pin_name = "pin{}".format(i+1) if (i+1) not in pin_names.keys() else pin_names[i+1]

            if i%2 == 1:
                button_column = 5
                name_column = 4
                picture_column = 3
                pin_image = pin_image_rotated_raw
            else:
                button_column = 0
                name_column = 1
                picture_column = 2
                pin_image = pin_image_raw

            row = i//2

            image_label = QLabel()
            image_label.setPixmap(pin_image)

            if (i+1) in pins_to_control:
                layout.addWidget(QPushButton('Toggle'), row, button_column)
            layout.addWidget(QLabel(pin_name), row, name_column)
            layout.addWidget(image_label, row, picture_column)

        self.horizontalGroupBox.setLayout(layout)

app = QApplication(sys.argv)
ex = Client()
sys.exit(app.exec_())
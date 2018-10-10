import sys
import socket
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QGridLayout, QLabel, QGroupBox
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from settings import pin_names, pins_to_control
from protocol import SetPin, Response, CheckPins, CheckPinsResponse, from_binary

HOST = '127.0.0.1'
PORT = 8888


class Communicate(QThread):
    received = pyqtSignal(bytes)

    def __init__(self, message):
        self.message = message
        self.HOST = HOST
        self.PORT = PORT
        super().__init__()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(self.message)
            data = s.recv(1024)
        self.received.emit(data)

class Client(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'RaspberryPi Controll'
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 500
        self.bulb_image_off = QPixmap('images/pin_off.png')
        self.bulb_image_on = QPixmap('images/pin_on.png')
        self.threads = []
        self.initUI()
        self.statuses = [0] * 40
        self.refresh_pin_statuses()

    def parse_response(self, data):
        response = from_binary(data)
        print('Received: {}'.format(response))

    def communicate_with_server(self, message):
        thread = Communicate(message)
        thread.received.connect(self.parse_response)
        thread.start()
        self.threads.append(thread)


    def refresh_pin_statuses(self):
        response = self.communicate_with_server(CheckPins().get_binary())
        # if isinstance(response, CheckPinsResponse):
        #     for pin, bulb in zip(response.statuses, self.bulbs):
        #         print(pin)
        #         print(bulb)
        #         bulb.setPixmap(self.bulb_image_on if pin else self.bulb_image_off)
        #         print(bulb.pixmap())
        #     self.statuses = response.statuses

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Connected to {}:{}".format(HOST, PORT))
        layout = QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(6, 1)
        layout.setColumnStretch(7, 1)
        layout.setColumnStretch(8, 1)

        pin_image_raw = QPixmap('images/pin.png')
        pin_image_rotated_raw = QPixmap('images/pin_rotated.png')

        self.bulbs = []

        for i in range(40):
            pin_name = "pin{}".format(i+1) if (i+1) not in pin_names.keys() else pin_names[i+1]

            if i%2 == 1:
                button_column = 7
                bulb_column = 6
                name_column = 5
                picture_column = 4
                pin_image = pin_image_rotated_raw
            else:
                button_column = 0
                bulb_column = 1
                name_column = 2
                picture_column = 3
                pin_image = pin_image_raw

            row = i//2

            image_label = QLabel()
            image_label.setPixmap(pin_image)
            bulb_label = QLabel()
            bulb_label.setPixmap(self.bulb_image_off)
            self.bulbs.append(bulb_label)

            layout.addWidget(bulb_label, row, bulb_column)
            if (i+1) in pins_to_control:
                toggle_button = QPushButton('Toggle')
                toggle_button.clicked.connect(partial(self.toggle_pin, i+1))
                layout.addWidget(toggle_button, row, button_column)
            layout.addWidget(QLabel(pin_name), row, name_column)
            layout.addWidget(image_label, row, picture_column)

        self.horizontalGroupBox.setLayout(layout)

    def toggle_pin(self, pin):
        set_pin_to_high = not self.statuses[pin-1]
        control_pin = SetPin(pin, set_pin_to_high).get_binary()
        self.communicate_with_server(control_pin)
        # if response.success:
        #     self.statuses[pin-1] = response.state
        #     self.bulbs[pin-1].setPixmap(self.bulb_image_on if response.state else self.bulb_image_off)

app = QApplication(sys.argv)
ex = Client()
sys.exit(app.exec_())

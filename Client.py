import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QMainWindow, QVBoxLayout, QGridLayout, QLabel, QGroupBox
from PyQt5.QtGui import QPainter, QPixmap
from settings import pin_names

class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        super().__init__()
        self.title = 'RaspberryPi Controll'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.setColumnStretch(3, 4)
        layout.setColumnStretch(4, 4)
        layout.setColumnStretch(5, 4)
        layout.setColumnStretch(6, 4)

        pin_image_raw =  QPixmap('/images/pin/png')
        pin_image_rotated_raw = QPixmap('/images/pin_rotated.png')

        for i in range(40):
            pin_name = "pin{}".format(i+1) if (i+1) not in pin_names.keys() else pin_names[i+1]

            if i%2 == 1:
                button_column = 5
                name_column = 4
                picture_column = 3
                pin_image = pin_image_raw
            else:
                button_column = 0
                name_column = 1
                picture_column = 2
                pin_image = pin_image_rotated_raw

            row = i//2

            image_label = QLabel()

            layout.addWidget(QPushButton('Toggle'), row, button_column)
            layout.addWidget(QLabel(pin_name), row, name_column)
            layout.addWidget(image_label.setPixmap(pin_image), row, picture_column)

        self.horizontalGroupBox.setLayout(layout)

app = QApplication(sys.argv)
ex = Client()
sys.exit(app.exec_())
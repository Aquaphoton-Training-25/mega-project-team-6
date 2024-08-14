import sys
import serial
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtCore import QTimer

########################################################
########################################################
########################################################

class CarControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # Adjust COM port as necessary

        # Timer for reading sensor values
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSensorValues)
        self.timer.start(1000)  # Update every second

    ########################################################
    ########################################################
    ########################################################

    def initUI(self):
        # Create layout and widgets
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout()

        #CHOOSE THE SPEED

        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(["LOW", "MEDIUM", "HIGH"])
        self.speedComboBox.currentIndexChanged.connect(self.changeSpeed)
        layout.addWidget(self.speedComboBox)

        #CHOOSE THE MODE

        self.modeComboBox = QComboBox()
        self.modeComboBox.addItems(["MANUAL", "AUTO"])
        self.modeComboBox.currentIndexChanged.connect(self.changeMode)
        layout.addWidget(self.modeComboBox)

        #FORWARD BUTTON

        self.forwardButton = QPushButton('Forward')
        self.forwardButton.clicked.connect(lambda: self.sendCommand("1"))
        layout.addWidget(self.forwardButton)

        #BACKWARD BUTTON

        self.backwardButton = QPushButton('Backward')
        self.backwardButton.clicked.connect(lambda: self.sendCommand("2"))
        layout.addWidget(self.backwardButton)

        #LEFT BUTTON

        self.leftButton = QPushButton('Left')
        self.leftButton.clicked.connect(lambda: self.sendCommand("4"))
        layout.addWidget(self.leftButton)

        #RIGHT BUTTON

        self.rightButton = QPushButton('Right')
        self.rightButton.clicked.connect(lambda: self.sendCommand("3"))
        layout.addWidget(self.rightButton)

        #STOP BUTTON

        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(lambda: self.sendCommand("0"))
        layout.addWidget(self.stopButton)

        #THE CURRENT VALUE

        self.currentLabel = QLabel("Current: ")
        layout.addWidget(self.currentLabel)

        #THE VOLTAGE VALUE

        self.voltageLabel = QLabel("Voltage: ")
        layout.addWidget(self.voltageLabel)

        self.centralWidget.setLayout(layout)

    ########################################################
    ########################################################
    ########################################################

    def sendCommand(self, command):
        #Send command to the Arduino
        self.serial.write(command.encode())
        time.sleep(0.1)  # Short delay for command processing

    ########################################################
    ########################################################
    ########################################################

    def updateSensorValues(self):

        #Read sensor values from the Arduino and update the GUI

        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode('utf-8').strip()
            if line.startswith("Current:"):
                self.currentLabel.setText(line)
            elif line.startswith("Voltage:"):
                self.voltageLabel.setText(line)

    ########################################################
    ########################################################
    ########################################################

    def changeSpeed(self):

        #Change speed based on user selection

        speed = self.speedComboBox.currentText().upper()
        self.serial.write(speed.encode())

    ########################################################
    ########################################################
    ########################################################

    def changeMode(self):

        #Change mode based on user selection

        mode = self.modeComboBox.currentText().upper()
        self.serial.write(mode.encode())

    ########################################################
    ########################################################
    ########################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CarControlApp()
    ex.show()
    sys.exit(app.exec())

                                ##################   AQUAPHOTON   #####################
                                ##################    HAPPY END   ######################
                                ##################    FIRMWARE    ####################
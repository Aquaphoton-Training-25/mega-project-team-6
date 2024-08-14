import sys
import serial
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer


# here we connect the desgin with the code
#####################################################
from my_gui import Ui_MainWindow  # Import the generated UI class
#####################################################

class CarControlApp(QtWidgets.QMainWindow, Ui_MainWindow):
    ##############################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Initialize the UI
        self.initUI()
        self.serial = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # bluetooth module serial connection by the port (COM4)

        # Timer for reading sensor values
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSensorValues)
        self.timer.start(1000)  # Update to avoid lose of data every second

    ##############################################################################

    def initUI(self):
        # CONNECT THE DESGIN TO THE FUNCTIONS

        #************************************************************************
        # SPEED BUTTONS
        self.low_pushButton.clicked.connect(lambda: self.changeSpeed("LOW"))
        self.medium_pushButton.clicked.connect(lambda: self.changeSpeed("MEDIUM"))
        self.high_pushButton.clicked.connect(lambda: self.changeSpeed("HIGH"))
        # ************************************************************************

        # ************************************************************************
        # MODE BUTTONS
        self.manual_pushButton.clicked.connect(lambda: self.changeMode("MANUAL"))
        self.auto_pushButton.clicked.connect(lambda: self.changeMode("AUTO"))
        # ************************************************************************

        # ************************************************************************
        # DIRECTION BUTTONS
        self.pushButton_.clicked.connect(lambda: self.sendCommand("1"))  # Forward
        self.down_pushButton.clicked.connect(lambda: self.sendCommand("2"))  # Backward
        self.left_pushButton.clicked.connect(lambda: self.sendCommand("4"))  # Left
        self.right_pushButton.clicked.connect(lambda: self.sendCommand("3"))  # Right
        # ************************************************************************

        # ************************************************************************
        # HANDLE THE VALUES WHEN CHANGED
        self.dial.valueChanged.connect(self.dialValueChanged)
        # ************************************************************************

    ##############################################################################
    ##############################################################################

    def sendCommand(self, command):
        # SEND COMMAND TO ARDUINO
        self.serial.write(command.encode())
        time.sleep(0.1)  # SHORT DELAY


    ##############################################################################
    ##############################################################################

    #READ OF CURRENT AND VOLTAGE SENSORS
    def updateSensorValues(self):
        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode('utf-8').strip()
            if line.startswith("Current:"):
                self.label_2.setText(line)
            elif line.startswith("Voltage:"):
                self.label_3.setText(line)

    ##############################################################################
    ##############################################################################

    #CHANGE OF SPEED(LOW , MEDIUM , HIGH)
    def changeSpeed(self, speed):
        # Change speed based on user selection
        self.serial.write(speed.encode())

    ##############################################################################
    ##############################################################################

    #CHANGE THE MODE( MANUAL , AUTONOMOUS )
    def changeMode(self, mode):
        # Change mode based on user selection
        self.serial.write(mode.encode())

    ##############################################################################
    ##############################################################################

    #HANDLE THE VALUES WHEN CHANGED
    def dialValueChanged(self, value):
        self.serial.write(str(value).encode())

    ##############################################################################
    ##############################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CarControlApp()
    MainWindow.show()
    sys.exit(app.exec())

    ######################  Aquaphoton ROV team   ##############################
    ######################         TEAM 6         ##############################
    ######################       HAPPY END        ##############################


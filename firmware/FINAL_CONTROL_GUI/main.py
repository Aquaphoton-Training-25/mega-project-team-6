import sys
import serial
import time
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer

# Import the generated UI classes
from my_gui import Ui_MainWindow
from Button_dialog import Ui_Button_dialog


class CarControlApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Initialize the UI
        self.initUI()
        self.serial = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # Connect to Bluetooth module

        # Timer for reading sensor values
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSensorValues)
        self.timer.start(1000)  # Update sensor values every second

    def initUI(self):
        # Connect the design to functions

        # Speed Buttons
        self.low_pushButton.clicked.connect(lambda: self.changeSpeed("LOW"))
        self.medium_pushButton.clicked.connect(lambda: self.changeSpeed("MEDIUM"))
        self.high_pushButton.clicked.connect(lambda: self.changeSpeed("HIGH"))

        # Mode Buttons
        self.manual_pushButton.clicked.connect(self.openbuttonsWindow)
        self.auto_pushButton.clicked.connect(lambda: self.changeMode("AUTO"))

        # Direction Buttons in the dialog window
        self.ui_buttons = Ui_Button_dialog()
        self.ui_buttons.setupUi(self)  # Set up the Button Dialog UI
        self.ui_buttons.up_pushButton.clicked.connect(lambda: self.sendCommand("1"))  # Forward
        self.ui_buttons.down_pushButton.clicked.connect(lambda: self.sendCommand("2"))  # Backward
        self.ui_buttons.left_pushButton.clicked.connect(lambda: self.sendCommand("4"))  # Left
        self.ui_buttons.right_pushButton.clicked.connect(lambda: self.sendCommand("3"))  # Right

        # Handle the dial value change
        self.ui_buttons.dial.valueChanged.connect(self.dialValueChanged)

    def sendCommand(self, command):
        # Send command to Arduino
        self.serial.write(command.encode())
        time.sleep(0.1)  # Short delay

    def updateSensorValues(self):
        # Read current and voltage sensors
        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode('utf-8').strip()
            if line.startswith("Current:"):
                self.label_2.setText(line)
            elif line.startswith("Voltage:"):
                self.label_3.setText(line)

    def changeSpeed(self, speed):
        # Change speed based on user selection
        self.serial.write(speed.encode())

    def changeMode(self, mode):
        # Change mode based on user selection
        self.serial.write(mode.encode())

    def dialValueChanged(self, value):
        # Handle the values when changed
        self.serial.write(str(value).encode())

    def openbuttonsWindow(self):
        # Open the Button Dialog Window
        self.window = QtWidgets.QDialog()
        self.ui_buttons.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CarControlApp()
    MainWindow.show()
    sys.exit(app.exec())

import sys
import serial
import time
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal

# Import the generated UI classes
from my_gui import Ui_MainWindow
from Button_dialog import Ui_Button_dialog
from auto_dialog import Ui_Dialog


class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port='COM6', baudrate=9600):
        super().__init__()
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.running = True

    def run(self):
        while self.running:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8').strip()
                self.data_received.emit(line)
            time.sleep(0.1)  # Avoid CPU overload

    def sendCommand(self, command):
        if self.serial.is_open:
            self.serial.write(command.encode() + b'\n')  # Ensure proper format with newline
            time.sleep(0.1)  # Short delay

    def stop(self):
        self.running = False
        if self.serial.is_open:
            self.serial.close()


class CarControlApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Start serial communication thread
        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.updateSensorValues)
        self.serial_thread.start()

        # Initialize the button dialog window as None
        self.button_dialog = None

    def initUI(self):
        # Connect the UI elements to their respective functions
        self.low_pushButton.clicked.connect(lambda: self.changeSpeed("LOW"))
        self.medium_pushButton.clicked.connect(lambda: self.changeSpeed("MEDIUM"))
        self.high_pushButton.clicked.connect(lambda: self.changeSpeed("HIGH"))

        self.manual_pushButton.clicked.connect(self.openbuttonsWindow)
        self.auto_pushButton.clicked.connect(self.openautoWindow)

    def updateSensorValues(self, line):
        # Update the GUI with the sensor values
        if line.startswith("Current:"):
            self.label.setText(line)
        elif line.startswith("Voltage:"):
            self.label_2.setText(line)

    def changeSpeed(self, speed):
        # Change speed based on user selection
        self.serial_thread.sendCommand(speed)

    def changeMode(self, mode):
        # Change mode based on user selection
        self.serial_thread.sendCommand(mode)

    def openbuttonsWindow(self):
        # Open the Button Dialog Window
        self.window = QtWidgets.QDialog()
        self.ui_buttons = Ui_Button_dialog()
        self.ui_buttons.setupUi(self.window)

        # Connect the direction buttons to send commands
        self.ui_buttons.up_pushButton.clicked.connect(lambda: self.sendCommand("1"))  # Forward
        self.ui_buttons.down_pushButton.clicked.connect(lambda: self.sendCommand("2"))  # Backward
        self.ui_buttons.left_pushButton.clicked.connect(lambda: self.sendCommand("4"))  # Left
        self.ui_buttons.right_pushButton.clicked.connect(lambda: self.sendCommand("3"))  # Right

        self.window.exec()  # Blocking call to keep the dialog open

    def sendCommand(self, command):
        # Send a command through the serial thread
        self.serial_thread.sendCommand(command)

    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()

    def openautoWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui_autonmous = Ui_Dialog()
        self.ui_autonmous.setupUi(self.window)

        # Connect the button to send the safe distance to Arduino
        self.ui_autonmous.pushButton_2.clicked.connect(self.sendSafeDistance)

        # Show the dialog
        self.window.exec()  # Blocking call to keep the dialog open

    def sendSafeDistance(self):
        # Get the safe distance value from QLineEdit
        distance = self.ui_autonmous.lineEdit_3.text().strip()

        # Validate and send the safe distance to Arduino
        if distance and distance.isdigit():
            self.serial_thread.sendCommand(f"S{distance}")  # Ensure proper format
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid distance.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CarControlApp()
    MainWindow.show()
    sys.exit(app.exec())

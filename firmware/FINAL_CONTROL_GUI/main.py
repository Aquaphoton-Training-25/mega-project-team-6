import sys
import serial
import time
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal

# Import the generated UI classes
from my_gui import Ui_MainWindow
from Button_dialog import Ui_Button_dialog
                                                        #########################################################
                                                        ################   HI AQUAPHOTON   ######################
                                                        #########################################################
class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port='COM4', baudrate=9600):
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
        self.serial.write(command.encode())
        time.sleep(0.1)  # Short delay

    def stop(self):
        self.running = False
        self.serial.close()


                                                        #########################################################
                                                        #########################################################
                                                        #########################################################
class CarControlApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Start serial communication thread
        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.updateSensorValues)
        self.serial_thread.start()

    def initUI(self):
        # Connect the UI elements to their respective functions
        self.low_pushButton.clicked.connect(lambda: self.changeSpeed("LOW"))
        self.medium_pushButton.clicked.connect(lambda: self.changeSpeed("MEDIUM"))
        self.high_pushButton.clicked.connect(lambda: self.changeSpeed("HIGH"))

        self.manual_pushButton.clicked.connect(self.openbuttonsWindow)
        self.auto_pushButton.clicked.connect(lambda: self.changeMode("AUTO"))

    def updateSensorValues(self, line):
        # Update the GUI with the sensor values
        if line.startswith("Current:"):
            self.label_2.setText(line)
        elif line.startswith("Voltage:"):
            self.label_3.setText(line)

    def changeSpeed(self, speed):
        # Change speed based on user selection
        self.serial_thread.sendCommand(speed)

    def changeMode(self, mode):
        # Change mode based on user selection
        self.serial_thread.sendCommand(mode)

    def dialValueChanged(self, value):
        # Handle the dial value change
        self.serial_thread.sendCommand(str(value))


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

        # Connect the dial value change to the appropriate method
        self.ui_buttons.dial.valueChanged.connect(self.dialValueChanged)

        # Show the dialog
        self.window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CarControlApp()
    MainWindow.show()
    sys.exit(app.exec())

                                                    #########################################################
                                                    ################   BYE AQUAPHOTON   #####################
                                                    #########################################################

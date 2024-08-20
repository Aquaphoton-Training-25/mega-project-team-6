import sys
import serial
import time
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal

# Import the generated UI classes
from my_gui import Ui_MainWindow
from Button_dialog import Ui_Button_dialog
from auto_dialog import Ui_Dialog

                                                    #########################################################
                                                    ################   HI AQUAPHOTON   ######################
                                                    #########################################################

class SerialThread(QThread):
    data_received = pyqtSignal(str)
    #PUT THE PORT OF THE ARDUINO 
    def __init__(self, port='COM4', baudrate=9600):
        super().__init__()
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.running = True

    def run(self):
        while self.running:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8').strip()
                self.data_received.emit(line)
            time.sleep(0.1)  #TO AVOID OVER LOAD(SHORT DELAY)

    def sendCommand(self, command):
        if self.serial.is_open:
            self.serial.write(command.encode() + b'\n')  
            time.sleep(0.1)  #TO AVOID OVER LOAD(SHORT DELAY)

    def stop(self):
        self.running = False
        if self.serial.is_open:
            self.serial.close()

class CarControlApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # START SERIAL COMMUNIACTION
        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.updateSensorValues)
        self.serial_thread.start()

    def initUI(self):
        #DETECT THE SPEED AND MODE BY PUSH THE BUTTONS (LOW , MEDIUM ,HIGH , MANUAL , AUTO)
        self.low_pushButton.clicked.connect(lambda: self.changeSpeed("LOW"))
        self.medium_pushButton.clicked.connect(lambda: self.changeSpeed("MEDIUM"))
        self.high_pushButton.clicked.connect(lambda: self.changeSpeed("HIGH"))

        self.manual_pushButton.clicked.connect(self.openButtonsWindow)
        self.auto_pushButton.clicked.connect(self.openAutoWindow)

    def updateSensorValues(self, line):
        # UPDATE SENSOR VALUES
        if line.startswith("Current:"):
            self.label_2.setText(line)
        elif line.startswith("Voltage:"):
            self.label_3.setText(line)

    def changeSpeed(self, speed):
        # CHANGE SPEED BY SELECT THE TRUE BUTTON
        self.serial_thread.sendCommand(speed)

    def changeMode(self, mode):
        # CHANGE MODE BY SELECT THE TRUE BUTTON
        self.serial_thread.sendCommand(mode)

    def openButtonsWindow(self):
        # Open the Button Dialog Window
        self.window = QtWidgets.QDialog()
        self.ui_buttons = Ui_Button_dialog()
        self.ui_buttons.setupUi(self.window)

        # SELECT THE DIRECTION
        self.ui_buttons.up_pushButton.clicked.connect(lambda: self.sendCommand("1"))  # Forward
        self.ui_buttons.down_pushButton.clicked.connect(lambda: self.sendCommand("2"))  # Backward
        self.ui_buttons.left_pushButton.clicked.connect(lambda: self.sendCommand("4"))  # Left
        self.ui_buttons.right_pushButton.clicked.connect(lambda: self.sendCommand("3"))  # Right

        self.window.exec()  

    def sendCommand(self, command):
        # SEND COMMAND THROUGH SERIAL
        self.serial_thread.sendCommand(command)

    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()

    def openAutoWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui_auto = Ui_Dialog()
        self.ui_auto.setupUi(self.window)

        # SEND THE SAFE DISTANCE
        self.ui_auto.pushButton_2.clicked.connect(self.sendSafeDistance)

        self.window.exec()  

    def sendSafeDistance(self):
        d = self.lineEdit_3.text().strip()

        print(f"Distance entered: '{d}'")  # Debug print

        if not d:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a distance.")
            return

        if d.isdigit():
            print(f"Sending command with distance: {d}")
            self.ui.pushButton_2.clicked.connect(self.sendSafeDistance)# Debug print
            self.sendToArduino(f"{d}\n")  # Send distance followed by newline
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid numeric distance.")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CarControlApp()
    MainWindow.show()
    sys.exit(app.exec())
    
                                                        #########################################################
                                                        ################   BYE AQUAPHOTON   #####################
                                                        #########################################################
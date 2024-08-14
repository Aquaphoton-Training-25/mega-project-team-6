import sys
import serial
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.ser = serial.Serial(port, baudrate)
        self.running = True

    def run(self):
        while self.running:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting).decode('utf-8')
                self.data_received.emit(data)

    def send_data(self, data):
        self.ser.write(data.encode())

    def stop(self):
        self.running = False
        self.ser.close()

class CarControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_thread = SerialThread('COM4', 9600)  # Replace 'COM3' with your Arduino's serial port
        self.serial_thread.data_received.connect(self.on_data_received)
        self.serial_thread.start()

    def initUI(self):
        self.setWindowTitle('Car Control')
        layout = QVBoxLayout()

        self.speed_label = QLabel('Choose Speed:')
        layout.addWidget(self.speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["LOW", "MEDIUM", "HIGH"])
        layout.addWidget(self.speed_combo)

        self.mode_label = QLabel('Choose Mode:')
        layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["MANUAL", "AUTO"])
        layout.addWidget(self.mode_combo)

        self.direction_label = QLabel('Manual Control (Only in MANUAL Mode):')
        layout.addWidget(self.direction_label)

        self.forward_btn = QPushButton('Forward')
        self.forward_btn.clicked.connect(lambda: self.send_command("1"))
        layout.addWidget(self.forward_btn)

        self.backward_btn = QPushButton('Backward')
        self.backward_btn.clicked.connect(lambda: self.send_command("2"))
        layout.addWidget(self.backward_btn)

        self.right_btn = QPushButton('Right')
        self.right_btn.clicked.connect(lambda: self.send_command("3"))
        layout.addWidget(self.right_btn)

        self.left_btn = QPushButton('Left')
        self.left_btn.clicked.connect(lambda: self.send_command("4"))
        layout.addWidget(self.left_btn)

        self.set_speed_btn = QPushButton('Set Speed')
        self.set_speed_btn.clicked.connect(self.set_speed)
        layout.addWidget(self.set_speed_btn)

        self.set_mode_btn = QPushButton('Set Mode')
        self.set_mode_btn.clicked.connect(self.set_mode)
        layout.addWidget(self.set_mode_btn)

        self.output_label = QLabel('')
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def set_speed(self):
        speed = self.speed_combo.currentText()
        self.send_command(speed)

    def set_mode(self):
        mode = self.mode_combo.currentText()
        self.send_command(mode)

    def send_command(self, command):
        self.serial_thread.send_data(command + '\n')

    def on_data_received(self, data):
        self.output_label.setText(data)

    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CarControlApp()
    ex.show()
    sys.exit(app.exec())

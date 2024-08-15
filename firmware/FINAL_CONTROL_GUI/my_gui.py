# my_gui.py
from PyQt6 import QtCore, QtWidgets
from Button_dialog import Ui_Button_dialog


class Ui_MainWindow(object):
    def openbuttonsWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Button_dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1166, 862)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 34);\n")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(480, -10, 191, 191))
        self.label.setStyleSheet("background-image: url(images/aqua.jfif);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 620, 541, 51))
        self.label_2.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n font: 75 italic 24pt \"Times New Roman\";")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(590, 620, 531, 51))
        self.label_3.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n font: 75 italic 24pt \"Times New Roman\";")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(600, 690, 521, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.low_pushButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.low_pushButton.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n font: 75 italic 20pt \"Times New Roman\";")
        self.low_pushButton.setCheckable(True)
        self.low_pushButton.setAutoExclusive(True)
        self.low_pushButton.setObjectName("low_pushButton")
        self.horizontalLayout.addWidget(self.low_pushButton)

        self.medium_pushButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.medium_pushButton.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n font: 75 italic 20pt \"Times New Roman\";")
        self.medium_pushButton.setCheckable(True)
        self.medium_pushButton.setAutoExclusive(True)
        self.medium_pushButton.setObjectName("medium_pushButton")
        self.horizontalLayout.addWidget(self.medium_pushButton)

        self.high_pushButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.high_pushButton.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n font: 75 italic 20pt \"Times New Roman\";")
        self.high_pushButton.setCheckable(True)
        self.high_pushButton.setAutoExclusive(True)
        self.high_pushButton.setObjectName("high_pushButton")
        self.horizontalLayout.addWidget(self.high_pushButton)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 680, 541, 111))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.manual_pushButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.manual_pushButton.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n font: 75 italic 20pt \"Times New Roman\";")
        self.manual_pushButton.setCheckable(True)
        self.manual_pushButton.setAutoExclusive(True)
        self.manual_pushButton.setObjectName("manual_pushButton")
        self.manual_pushButton.clicked.connect(self.openbuttonsWindow)
        self.horizontalLayout_2.addWidget(self.manual_pushButton)

        self.auto_pushButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.auto_pushButton.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n font: 75 italic 20pt \"Times New Roman\";")
        self.auto_pushButton.setCheckable(True)
        self.auto_pushButton.setAutoExclusive(True)
        self.auto_pushButton.setObjectName("auto_pushButton")
        self.horizontalLayout_2.addWidget(self.auto_pushButton)

        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(560, 620, 20, 141))
        self.line_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"justify\"><br/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "MODE"))
        self.label_3.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"justify\"><br/></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Speed"))
        self.low_pushButton.setText(_translate("MainWindow", "Low"))
        self.medium_pushButton.setText(_translate("MainWindow", "Medium"))
        self.high_pushButton.setText(_translate("MainWindow", "High"))
        self.manual_pushButton.setText(_translate("MainWindow", "Manual"))
        self.auto_pushButton.setText(_translate("MainWindow", "Autonomous"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

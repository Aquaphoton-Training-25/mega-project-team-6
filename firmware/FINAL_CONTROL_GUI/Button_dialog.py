from PyQt6 import QtCore, QtGui, QtWidgets
                                                    #########################################################
                                                    ################   HI AQUAPHOTON   ######################
                                                    #########################################################
class Ui_Button_dialog(object):
    def setupUi(self, Button_dialog):
        Button_dialog.setObjectName("Button_dialog")
        Button_dialog.resize(800, 600)
        Button_dialog.setStyleSheet("background-color: rgb(0, 0, 34);")

        self.dial = QtWidgets.QDial(parent=Button_dialog)
        self.dial.setGeometry(QtCore.QRect(220, 150, 81, 71))
        self.dial.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dial.setObjectName("dial")

        #####################################################
        # Down Button with Image
        #####################################################

        self.down_pushButton = QtWidgets.QPushButton(parent=Button_dialog)
        self.down_pushButton.setGeometry(QtCore.QRect(230, 240, 61, 121))
        self.down_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.down_pushButton.setText("")
        down_icon = QtGui.QIcon(QtGui.QPixmap(r"C:\Users\KimoStore\Downloads\FINAL_CONTROL_GUI\images\images\down.png"))
        self.down_pushButton.setIcon(down_icon)
        self.down_pushButton.setIconSize(QtCore.QSize(80, 65))
        self.down_pushButton.setCheckable(True)
        self.down_pushButton.setAutoExclusive(True)
        self.down_pushButton.setObjectName("down_pushButton")


        #####################################################
        # Right Button with Image
        #####################################################


        self.right_pushButton = QtWidgets.QPushButton(parent=Button_dialog)
        self.right_pushButton.setGeometry(QtCore.QRect(340, 130, 121, 61))
        self.right_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.right_pushButton.setText("")
        right_icon = QtGui.QIcon(QtGui.QPixmap(r"C:\Users\KimoStore\Downloads\FINAL_CONTROL_GUI\images\images\right.png"))
        self.right_pushButton.setIcon(right_icon)
        self.right_pushButton.setIconSize(QtCore.QSize(80, 65))
        self.right_pushButton.setCheckable(True)
        self.right_pushButton.setAutoExclusive(True)
        self.right_pushButton.setObjectName("right_pushButton")


        #####################################################
        # Up Button with Image
        #####################################################


        self.up_pushButton = QtWidgets.QPushButton(parent=Button_dialog)
        self.up_pushButton.setGeometry(QtCore.QRect(230, 0, 61, 121))
        self.up_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.up_pushButton.setText("")
        up_icon = QtGui.QIcon(QtGui.QPixmap(r"C:\Users\KimoStore\Downloads\FINAL_CONTROL_GUI\images\images\up.png"))
        self.up_pushButton.setIcon(up_icon)
        self.up_pushButton.setIconSize(QtCore.QSize(65, 50))
        self.up_pushButton.setCheckable(True)
        self.up_pushButton.setAutoExclusive(True)
        self.up_pushButton.setObjectName("up_pushButton")

        #####################################################
        # Left Button with Image
        #####################################################

        self.left_pushButton = QtWidgets.QPushButton(parent=Button_dialog)
        self.left_pushButton.setGeometry(QtCore.QRect(90, 130, 121, 61))
        self.left_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.left_pushButton.setText("")
        left_icon = QtGui.QIcon(QtGui.QPixmap(r"C:\Users\KimoStore\Downloads\FINAL_CONTROL_GUI\images\images\left.png"))
        self.left_pushButton.setIcon(left_icon)
        self.left_pushButton.setIconSize(QtCore.QSize(80, 65))
        self.left_pushButton.setCheckable(True)
        self.left_pushButton.setAutoExclusive(True)
        self.left_pushButton.setObjectName("left_pushButton")

        self.retranslateUi(Button_dialog)
        QtCore.QMetaObject.connectSlotsByName(Button_dialog)

    def retranslateUi(self, Button_dialog):
        _translate = QtCore.QCoreApplication.translate
        Button_dialog.setWindowTitle(_translate("Button_dialog", "Dialog"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Button_dialog = QtWidgets.QDialog()
    ui = Ui_Button_dialog()
    ui.setupUi(Button_dialog)
    Button_dialog.show()
    sys.exit(app.exec())

                                                        #########################################################
                                                        ################   BYE AQUAPHOTON   #####################
                                                        #########################################################


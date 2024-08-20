import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QFileDialog, QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import stitch_backend
import stereoVision


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1166, 862)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 34);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stitch_backend = stitch_backend.StitchBackend()
        main_layout = QVBoxLayout(self.centralwidget)

        #button
        self.stitchButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.stitchButton.setStyleSheet("background-color:white;")
        self.stitchButton.setText("Video Stitching")
        self.stitchButton.setFixedSize(150, 25)
        self.stitchButton.clicked.connect(self.stitch_backend.stitch_videos)
        main_layout.addWidget(self.stitchButton)


        def on_stitchButton_clicked(self):
            leftVideo, _ = QFileDialog.getOpenFileName(None, "Select Left Video")
            rightVideo, _ = QFileDialog.getOpenFileName(None, "Select Right Video")
            self.player1.setSource(QUrl.fromLocalFile(leftVideo))
            self.player2.setSource(QUrl.fromLocalFile(rightVideo))

            self.stitch_backend.stitch_videos()


            output_path = "outputStitched_new.mp4"

            self.player3.setSource(QUrl.fromLocalFile(output_path))
            self.player3.play()

        video_layout1 = QHBoxLayout()
        main_layout.addLayout(video_layout1)
        self.video_widget1 = QVideoWidget()
        self.video_widget1.setFixedSize(200, 240) 
        video_widget1_layout = QVBoxLayout()
        video_widget1_layout.addWidget(self.video_widget1)
        video_widget1_layout.setContentsMargins(0, 0, 0, 0) 
        video_layout1.addLayout(video_widget1_layout)

        self.video_widget2 = QVideoWidget()
        self.video_widget2.setFixedSize(200, 240)  
        video_widget2_layout = QVBoxLayout()
        video_widget2_layout.addWidget(self.video_widget2)
        video_widget2_layout.setContentsMargins(0, 0, 700, 0) 
        video_layout1.addLayout(video_widget2_layout)

        video_layout2 = QVBoxLayout()
        main_layout.addLayout(video_layout2)

        self.video_widget3 = QVideoWidget()
        self.video_widget3.setFixedSize(420, 150) 
        video_widget3_layout = QVBoxLayout()
        video_widget3_layout.addWidget(self.video_widget3)
        video_widget3_layout.setContentsMargins(15, 0, 20, 20) 
        video_layout2.addLayout(video_widget3_layout)

        # Set the QMediaPlayer
        self.player1 = QMediaPlayer()


        self.player2 = QMediaPlayer()


        self.player3 = QMediaPlayer()


        on_stitchButton_clicked(self)

        self.player1.play()
        self.player2.play()
        self.player3.play()


        self.label_2 = QtWidgets.QLabel()
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 34); font: 75 italic 24pt 'Times New Roman';")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_2)

        self.label_3 = QtWidgets.QLabel()
        self.label_3.setStyleSheet("background-color: rgb(0, 0, 34); font: 75 italic 24pt 'Times New Roman';")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_3)
        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

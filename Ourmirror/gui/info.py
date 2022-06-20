
from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt
import time
import PIL
from PIL import Image,ImageDraw,ImageFont
import os
from gui import btn_control

def init_info(self,MainWindow):
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./font/Lobster-Regular.ttf')
    fontDB.addApplicationFont('./font/NanumGothic-Bold.ttf')
    
    #time 이라는 이름으로 label 생성 [(오전/오후)시/분]
    self.time = QtWidgets.QLabel(self.centralwidget)
    self.time.setGeometry(QtCore.QRect(1590,850,800,200))
    self.time.setObjectName("time")
    self.time.setAlignment(Qt.AlignLeft)
    #setFont(QtGui.QFont("Font_name",Font_size))
    self.time.setFont(QtGui.QFont("NanumGothic",70)) 
    self.time.setStyleSheet("Color : #FFFFFF;\
                              font-weight : 700;")

    #date 이라는 이름으로 label 생성 [년/월/일]
    self.date = QtWidgets.QLabel(self.centralwidget)
    self.date.setGeometry(QtCore.QRect(1580, 780, 5000, 100))
    self.date.setObjectName("date")
    self.date.setAlignment(Qt.AlignLeft)
    self.date.setFont(QtGui.QFont("NanumGothic",40))
    self.date.setStyleSheet("Color : #FFFFFF;\
                            font-weight : 100;")

    #title
    self.title = QtWidgets.QLabel(self.centralwidget)
    self.title.setGeometry(QtCore.QRect(1500,950,10,60))
    pixmap = QtGui.QPixmap(f"./font/icon.png")
    self.title.setAlignment(Qt.AlignLeft)
    self.title.setPixmap(QPixmap(pixmap))
    self.title.resize(444,138)

    self.infomation_txt = QtWidgets.QLabel(self.centralwidget)
    self.infomation_txt.setGeometry(QtCore.QRect(550, 300, 1000, 300))
    self.infomation_txt.setObjectName("info")
    self.infomation_txt.setFont(QtGui.QFont("NanumGothic",45))
    self.infomation_txt.setAlignment(Qt.AlignLeft)
    self.infomation_txt.setStyleSheet("Color : #FFFFFF;\
                                     font-weight : 700;")


    self.voice_info_icon = QtWidgets.QLabel(self.centralwidget)
    self.voice_info_icon.setGeometry(QtCore.QRect(20,100,10,60))
    pixmap = QtGui.QPixmap(f"./font/speaker.png")
    pixmap = pixmap.scaledToWidth(60)
    self.voice_info_icon.setAlignment(Qt.AlignLeft)
    self.voice_info_icon.setPixmap(QPixmap(pixmap))
    self.voice_info_icon.resize(60,60)


    self.voice_info = QtWidgets.QLabel(self.centralwidget)
    self.voice_info.setGeometry(QtCore.QRect(90, 100, 500, 800))
    self.voice_info.setObjectName("info")
    self.voice_info.setFont(QtGui.QFont("NanumGothic",35))
    self.voice_info.setAlignment(Qt.AlignLeft)
    self.voice_info.setStyleSheet("Color : #FFFFFF;\
                                    font-weight : 700;")

    self.voice_info_txt = QtWidgets.QLabel(self.centralwidget)
    self.voice_info_txt.setGeometry(QtCore.QRect(20, 200, 500, 800))
    self.voice_info_txt.setObjectName("info")
    self.voice_info_txt.setFont(QtGui.QFont("NanumGothic",32))
    self.voice_info_txt.setAlignment(Qt.AlignLeft)
    self.voice_info_txt.setStyleSheet("Color : #FFFFFF;\
                                    font-weight : 100;")

    self.voice_info_value = QtWidgets.QLabel(self.centralwidget)
    self.voice_info_value.setGeometry(QtCore.QRect(70, 270, 500, 800))
    self.voice_info_value.setObjectName("info")
    self.voice_info_value.setFont(QtGui.QFont("NanumGothic",32))
    self.voice_info_value.setAlignment(Qt.AlignLeft)
    self.voice_info_value.setStyleSheet("Color : #FFFFFF;\
                                    font-weight : 700;")


    
    btn_control.main_page_voice_info(self,MainWindow)


def set_info_data(self,MainWindow,data):

    info = "음성 인식 안내"
    txt = ""
    value = ""

    for i in data:
    
        txt = txt + f"{i[0]}\n\n\n\n"
        value = value + f" \"{i[1]}\"\n\n\n\n"


    pixmap = QtGui.QPixmap(f"./font/speaker.png")
    pixmap = pixmap.scaledToWidth(60)
    self.voice_info_icon.setPixmap(QPixmap(pixmap))

    
    self.voice_info.setText(info)
    self.voice_info_txt.setText(txt)
    self.voice_info_value.setText(value)

def wait_info_data(self,MainWindow):

    pixmap = QtGui.QPixmap(f"./font/stop_speaker.png")
    pixmap = pixmap.scaledToWidth(60)
    self.voice_info_icon.setPixmap(QPixmap(pixmap))


    self.voice_info.setText("음성 인식 일시정지")
    self.voice_info_txt.setText("")
    self.voice_info_value.setText("")


def txt_print(self,MainWindow):

    while(1):
        self.infomation_txt.setText(self.info_data)
        if self.txt_timer > 0:
            self.txt_timer = self.txt_timer - 1

        elif self.txt_timer == 0:
            self.txt_timer = -1
            self.info_data = ""

        time.sleep(0.2)
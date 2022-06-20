from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
from mqtt_client import image_send,hair_setting_send
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtWidgets import QPushButton
from gui import btn_control, info
import mqtt_client
import sys
from user import status_check
from PIL import Image,ImageDraw,ImageFont
import os

fontsFolder = './font' 
people_type = ""
hair_type = ""
chart_img_location = "./temp/trend_chart/"
hair_img_location = "./temp/trend_image/"
voice_text = ""

chart_now = None
photos = []
image_choice_num = 0

def init_trend(self, MainWindow):

    self.men_cut_chart = QtWidgets.QLabel(self.centralwidget)
    self.men_cut_chart.setGeometry(QtCore.QRect(550,50,10,60))
    self.men_cut_chart.resize(0,0)

    self.men_perm_chart = QtWidgets.QLabel(self.centralwidget)
    self.men_perm_chart.setGeometry(QtCore.QRect(550,50,10,60))
    self.men_perm_chart.resize(0,0)

    self.women_cut_chart = QtWidgets.QLabel(self.centralwidget)
    self.women_cut_chart.setGeometry(QtCore.QRect(550,50,10,60))
    self.women_cut_chart.resize(0,0)

    self.women_perm_chart = QtWidgets.QLabel(self.centralwidget)
    self.women_perm_chart.setGeometry(QtCore.QRect(550,50,10,60))
    self.women_perm_chart.resize(0,0)

    gif = QMovie(f'{chart_img_location}man_cut.gif')
    self.men_cut_chart.setMovie(gif) # use setMovie function in our QLabel
    self.men_cut_chart.setMaximumWidth(900)
    gif.start()

    gif = QMovie(f'{chart_img_location}man_perm.gif')
    self.men_perm_chart.setMovie(gif) # use setMovie function in our QLabel
    self.men_perm_chart.setMaximumWidth(900)
    gif.start()

    gif = QMovie(f'{chart_img_location}woman_cut.gif')
    self.women_cut_chart.setMovie(gif) # use setMovie function in our QLabel
    self.women_cut_chart.setMaximumWidth(900)
    gif.start()

    gif = QMovie(f'{chart_img_location}woman_perm.gif')
    self.women_perm_chart.setMovie(gif) # use setMovie function in our QLabel
    self.women_perm_chart.setMaximumWidth(900)
    gif.start()

def start_trend(self, MainWindow):
    text = "        추천받을 헤어스타일의\n          종류를 말씀해주세요."
    self.set_txt(text)

    self.voice_status_setting(text,"init_trend")

    btn_control.init_hair_trend(self, MainWindow)
    pass

def select_trend(self, MainWindow, type_set):
    global people_type, hair_type
    people_type = self.user_type
    hair_type = type_set

    self.trend_thread(MainWindow)


def trend_hair(self,MainWindow):
    global people_type, chart_img_location, voice_text, hair_type, chart_now

    if people_type == "man":
        if hair_type == "cut":

            self.set_txt("")
            text = "\
        현재 유행하는 남성 컷트 헤어스타일 그래프입니다.\
        1위는 아이비리그컷, 2위는 가일컷, 3위는 댄디컷, 4위는 드롭컷입니다.\
        다시 들으시려면 \"다시 말해줘\". \
        헤어스타일 사진을 보고 싶으면 \"사진 보여줘\".\
        처음으로 가시려면 \"메인화면\"이라고 말씀해주세요."

            self.men_cut_chart.resize(900,900)
            self.men_cut_chart.show()
            chart_now = self.men_cut_chart

        if hair_type == "perm":

            self.set_txt("")
            text = "\
        현재 유행하는 남성 펌 헤어스타일 그래프입니다.\
        1위는 에즈펌, 2위는 다운펌, 3위는 가르마 펌, 4위는 가일펌입니다.\
        다시 들으시려면 \"다시 말해줘\". \
        헤어스타일 사진을 보고 싶으면 \"사진 보여줘\".\
        처음으로 가시려면 \"메인화면\"이라고 말씀해주세요."

            self.men_perm_chart.resize(900,900)
            self.men_perm_chart.show()
            chart_now = self.men_perm_chart

    if people_type == "woman":
        if hair_type == "cut":

            self.set_txt("")
            text = "\
        현재 유행하는 여성 커트 헤어스타일 그래프입니다.\
        1위는 레이어드컷, 2위는 숏컷, 3위는 허쉬컷, 4위는 테슬컷입니다.\
        다시 들으시려면 \"다시 말해줘\". \
        헤어스타일 사진을 보고 싶으면 \"사진 보여줘\".\
        처음으로 가시려면 \"메인화면\"이라고 말씀해주세요."

            self.women_cut_chart.resize(900,900)
            self.women_cut_chart.show()
            chart_now = self.women_cut_chart

        if hair_type == "perm":

            self.set_txt("")
            text = "\
        현재 유행하는 여성 펌 헤어스타일 그래프입니다.\
        1위는 웨이브펌, 2위는 러블리펌, 3위는 레이어드 펌, 4위는 루즈펌입니다.\
        다시 들으시려면 \"다시 말해줘\". \
        헤어스타일 사진을 보고 싶으면 \"사진 보여줘\".\
        처음으로 가시려면 \"메인화면\"이라고 말씀해주세요."

            self.women_perm_chart.resize(900,900)
            self.women_perm_chart.show()
            chart_now = self.women_perm_chart



    voice_text = text
    self.voice_status_setting(text,"chart_trend")

    sleep(0.01)

    # 메인 화면으로 돌아가기
    btn_control.end_trend_info(self,MainWindow)

    sys.exit(0)

def voice_retry(self,MainWindow):
    self.voice_status_setting(voice_text,"chart_trend")

def trend_img_show(self,MainWindow):
    global chart_now, photos

    chart_now.hide()

    photos = [self.photo1,self.photo2,self.photo3,self.photo4]

    text = "\
    미용하실 헤어스타일의 번호를 말씀해 주세요.\
    처음으로 돌아가시려면 \"메인화면\" 이라고 말씀해 주세요."

    self.voice_status_setting(text,"img_trend")

    num = 1

    image_numbering()

    for i in photos:
        file_name = f"{people_type}_{hair_type}" + f"{num}"
        pixmap = QtGui.QPixmap(f"{hair_img_location}{file_name}.jpg")
        pixmap = pixmap.scaledToWidth(450)
        i.setPixmap(QPixmap(pixmap))
        i.resize(450,450)
        i.show()
        num = num+1
        sleep(0.01)

    btn_control.hairimg_trend_info(self,MainWindow)

def image_numbering():

    x = 1
    for i in range(4) :
        file_name = f"{people_type}_{hair_type}" + f"{x}"
        target_image = Image.open(f'{hair_img_location}{file_name}.jpg')  #일단 기본배경폼 이미지를 open 합니다.
        selectedFont =ImageFont.truetype(os.path.join(fontsFolder,'font.ttf'),80) #폰트경로과 사이즈를 설정해줍니다.
        draw =ImageDraw.Draw(target_image)

        height_ratio = target_image.size[1]-450
        height_ratio = height_ratio/2

        num_height = target_image.size[1]-height_ratio-90
        img_bottom = target_image.size[1]-height_ratio

        draw.rectangle([(0, img_bottom-100), (100, img_bottom)], fill=(0, 0, 0))
        draw.text((20,num_height),f'{x}',fill="white",font=selectedFont,align='center') # fill= 속성은 무슨 색으로 채울지 설정,font=는 자신이 설정한 폰트 설정

        x = x+1

        test = target_image.convert('RGB')

        test.save(f"{hair_img_location}{file_name}.jpg") #편집된 이미지를 저장합니다.

        target_image.close()
        test.close()

def choice_img(self,MainWindow,number):
    global photos, image_choice_num

    file_name = f"{people_type}_{hair_type}" + f"{number}"
    target_image = Image.open(f'{hair_img_location}{file_name}.jpg')  #일단 기본배경폼 이미지를 open 합니다.
    selectedFont =ImageFont.truetype(os.path.join(fontsFolder,'font.ttf'),50) #폰트경로과 사이즈를 설정해줍니다.
    draw =ImageDraw.Draw(target_image)


    # 선택된 사진 테두리 표시
    height_ratio = target_image.size[1]-450
    height_ratio = height_ratio/2

    height_top = height_ratio
    height_bottom = target_image.size[1] - height_ratio
    weight = 450

    draw.line((0, height_top, 0, height_bottom), fill="yellow", width=10)
    draw.line((0, height_bottom, weight, height_bottom), fill="yellow", width=10)
    draw.line((weight, height_top, weight, height_bottom), fill="yellow", width=10)
    draw.line((0, height_top, weight, height_top), fill="yellow", width=10)

    #선택된 사진 번호 색깔 변경
    num_height = target_image.size[1]-height_ratio-90

    selectedFont =ImageFont.truetype(os.path.join(fontsFolder,'font.ttf'),80) #폰트경로과 사이즈를 설정해줍니다.
    draw.text((20,num_height),f'{number}',fill="yellow",font=selectedFont,align='center') # fill= 속성은 무슨 색으로 채울지 설정,font=는 자신이 설정한 폰트 설정

    test = target_image.convert('RGB')

    test.save(f"{hair_img_location}choice.jpg") #편집된 이미지를 저장합니다.

    target_image.close()
    test.close()

    sleep(0.01)

    pixmap = QtGui.QPixmap(f"{hair_img_location}choice.jpg")
    pixmap = pixmap.scaledToWidth(450)
    photos[number-1].setPixmap(QPixmap(pixmap))
    photos[number-1].resize(450,450)
    photos[number-1].show()
    sleep(0.01)

    image_choice_num = number

    text = f"{number}번을 선택하셨습니다. 맞으면 확인, 다르면 취소라 말씀해 주세요."
    self.voice_status_setting(text,"choice_hair_trend")

    btn_control.choice_num_check(self,MainWindow)

def cancel_choice_trend(self,MainWindow):
    global image_choice_num

    file_name = f"{people_type}_{hair_type}" + f"{image_choice_num}"
    pixmap = QtGui.QPixmap(f"{hair_img_location}{file_name}.jpg")
    pixmap = pixmap.scaledToWidth(450)
    photos[image_choice_num-1].setPixmap(QPixmap(pixmap))
    photos[image_choice_num-1].resize(450,450)
    photos[image_choice_num-1].show()
    sleep(0.01)

    text = f"취소했습니다. 다른 번호를 선택하시거나 기능을 말씀해 주세요."
    self.voice_status_setting(text,"img_trend")
    image_choice_num = 0
    btn_control.hairimg_trend_info(self,MainWindow)
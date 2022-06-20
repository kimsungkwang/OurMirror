from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
from image import pi_camera
from mqtt_client import image_send,hair_setting_send
from picamera import PiCamera
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtWidgets import QPushButton
from gui import btn_control, info
from PIL import Image,ImageDraw,ImageFont
from PyQt5.QtCore import Qt
import mqtt_client
import sys
import os

from user import status_check
fontsFolder = './font'    #글자로 쓸 폰트 경로
return_hair_location = "./temp/return_image/"

hair_data = {
    'person_type' : '',
    'hair_type' : ''
}

photos = []


image_choice_num = 0

json_save = {}
emotion = {}


def init_hair_gui(self,MainWindow):
    global photos

    self.camera_timer = QtWidgets.QLabel(self.centralwidget)
    self.camera_timer.setGeometry(QtCore.QRect(600, 200, 1000, 500))
    self.camera_timer.setObjectName("info")
    self.camera_timer.setFont(QtGui.QFont("맑은 고딕",200))
    self.camera_timer.setStyleSheet("Color : #ffffff")

    self.photo1 = QtWidgets.QLabel(self.centralwidget)
    self.photo1.setGeometry(QtCore.QRect(500,150,10,60))
    self.photo1.resize(0,0)

    self.photo2 = QtWidgets.QLabel(self.centralwidget)
    self.photo2.setGeometry(QtCore.QRect(970,150,10,60))
    self.photo2.resize(0,0)

    self.photo3 = QtWidgets.QLabel(self.centralwidget)
    self.photo3.setGeometry(QtCore.QRect(500,600,10,60))
    self.photo3.resize(0,0)

    self.photo4 = QtWidgets.QLabel(self.centralwidget)
    self.photo4.setGeometry(QtCore.QRect(970,600,10,60))
    self.photo4.resize(0,0)


    photos.append(self.photo1)
    photos.append(self.photo2)
    photos.append(self.photo3)
    photos.append(self.photo4)


    self.cut_img = QtWidgets.QLabel(self.centralwidget)
    self.cut_img.setGeometry(QtCore.QRect(600,300,10,60))
    self.cut_img.resize(0,0)

    self.perm_img = QtWidgets.QLabel(self.centralwidget)
    self.perm_img.setGeometry(QtCore.QRect(1000,300,10,60))
    self.perm_img.resize(0,0)

    self.loading = QtWidgets.QLabel(self.centralwidget)
    self.loading.setGeometry(QtCore.QRect(830,300,10,60))
    self.loading.resize(0,0)

    gif = QMovie('./font/loading.gif')
    self.loading.setMovie(gif) # use setMovie function in our QLabel
    self.loading.setMaximumWidth(400)
    gif.start()

    self.face_type = QtWidgets.QLabel(self.centralwidget)
    self.face_type.setGeometry(QtCore.QRect(1450, 150, 1000, 600))
    self.face_type.setObjectName("info")
    self.face_type.setFont(QtGui.QFont("맑은 고딕",29))
    self.face_type.setAlignment(Qt.AlignLeft)
    self.face_type.setStyleSheet("Color : #FFFFFF;\
                                  font-weight : 400;")

    self.face_type_value = QtWidgets.QLabel(self.centralwidget)
    self.face_type_value.setGeometry(QtCore.QRect(1470, 220, 1000, 600))
    self.face_type_value.setObjectName("info")
    self.face_type_value.setFont(QtGui.QFont("맑은 고딕",29))
    self.face_type_value.setAlignment(Qt.AlignLeft)
    self.face_type_value.setStyleSheet("Color : #FFFFFF;\
                                  font-weight : 700;")

    self.emotion_img = QtWidgets.QLabel(self.centralwidget)
    self.emotion_img.setGeometry(QtCore.QRect(1800,150,10,60))
    self.emotion_img.resize(0,0)

def json_val_save(json_val):
    global json_save
    json_save = json_val
    print(json_save)

def emotion_recv(data):
    global emotion
    emotion = data
    print(emotion)


def face_scan(self,MainWindow):
    global json_save
    json_save = {}

    self.infomation_txt.setGeometry(QtCore.QRect(550, 200, 1000, 300))
    text = "     - 커트 혹은 펌을 선택해 주세요 -"
    self.set_txt(text)

    self.voice_status_setting(text,"init_hair")
    btn_control.init_hair_voice_info(self,MainWindow)

    pixmap = QtGui.QPixmap(f"./font/cut1.png")
    pixmap = pixmap.scaledToWidth(450)
    self.cut_img.setPixmap(QPixmap(pixmap))
    self.cut_img.resize(450,450)
    self.cut_img.show()

    pixmap = QtGui.QPixmap(f"./font/perm1.png")
    pixmap = pixmap.scaledToWidth(450)
    self.perm_img.setPixmap(QPixmap(pixmap))
    self.perm_img.resize(450,450)
    self.perm_img.show()

def start_camera(self,MainWindow,user_hair):
    if status_check() == 0:
        return

    
    if(user_hair == "cut"):
        text = "커트를 선택하셨습니다."

        self.voice_status_setting(text,"wait")

        pixmap = QtGui.QPixmap(f"./font/cut2.png")
        pixmap = pixmap.scaledToWidth(450)
        self.cut_img.setPixmap(QPixmap(pixmap))

        pixmap = QtGui.QPixmap(f"./font/perm3.png")
        pixmap = pixmap.scaledToWidth(450)
        self.perm_img.setPixmap(QPixmap(pixmap))

    if(user_hair == "perm"):
        text = "펌을 선택하셨습니다."

        self.voice_status_setting(text,"wait")

        pixmap = QtGui.QPixmap(f"./font/cut3.png")
        pixmap = pixmap.scaledToWidth(450)
        self.cut_img.setPixmap(QPixmap(pixmap))

        pixmap = QtGui.QPixmap(f"./font/perm2.png")
        pixmap = pixmap.scaledToWidth(450)
        self.perm_img.setPixmap(QPixmap(pixmap))

    sleep(2.3)
    self.cut_img.hide()
    self.perm_img.hide()
    self.set_txt("")
    sleep(0.2)
    self.infomation_txt.setGeometry(QtCore.QRect(550, 300, 1000, 300))

    self.window_status = "wait"
    self.user_hair = user_hair
    self.face_scan_timer = 600
    
    text = "     사진 촬영을 하겠습니다.\n       정면을 바라봐 주세요"
    self.voice_status_setting(text,"wait")
    self.camera_start(MainWindow)
    # for i in range(3,0,-1):
    #     self.camera_timer.setText(i)

    
def thread_camera(self,MainWindow):
    global photos,return_hair_location,image_choice_num, json_save

    info.wait_info_data(self,MainWindow)

    hair_setting_send(self,MainWindow)
    self.mqtt_status = 1
    self.mqtt_recv_end = 0
    self.video_stop == 1

    self.camera_timer.show()
    for i in range(4,0,-1):
        self.camera_timer.setText(f"    {i}")
        sleep(1)
    self.camera_timer.hide()


    
    pi_camera()
    image_send(self,MainWindow)
    

    text = "얼굴 분석중 입니다. 잠시만 기달려 주세요"

    self.voice_status_setting(text,"wait")

    self.loading.resize(400,400)
    self.loading.show()
    

    for i in range(10):
        sleep(1)
        if self.mqtt_recv_end == 1:
            break
    
    self.loading.hide()        

    self.mqtt_recv_end = 0
    self.mqtt_status = 0    
    self.video_stop == 0

        

    # if json_save == {}:
    #     json_save = {
    #        'face_shape' : '- 테스트중',
    #        'before_hair' : '- 테스트중'
    #     }

    if json_save != {}:

        self.face_type.setText(f"\
{self.user_name}님의 얼굴형\n\n\n\n\
{self.user_name}님의 현재 헤어스타일")

        self.face_type_value.setText(f"\
    - {json_save['face_shape']}\n\n\n\n\
    - {json_save['before_hair']}")

        self.face_type.show()
        self.face_type_value.show()



        self.set_txt("")
        text = "\
    헤어 추천이 완료되었습니다. \
    미용하실 헤어스타일의 번호를 말씀해 주세요.\
    헤어스타일 안내가 필요하시면 \"설명해줘\" 라고 말씀해 주세요.\
    처음으로 돌아가시려면 \"메인화면\" 이라고 말씀해 주세요."


        self.voice_status_setting(text,"show_hair")
        sleep(0.3)
        #self.infomation_txt.setGeometry(QtCore.QRect(750, 170, 1000, 300))

        image_numbering()

        num = 1
        for i in photos:
            file_name = "test" + f"{num}"
            pixmap = QtGui.QPixmap(f"{return_hair_location}{file_name}.jpg")
            pixmap = pixmap.scaledToWidth(450)
            i.setPixmap(QPixmap(pixmap))
            i.resize(450,450)
            i.show()
            num = num+1
            sleep(0.01)

        image_choice_num = 0
        btn_control.end_hair_voice_info(self,MainWindow)

    else : 
        txt = "서버와 연결 실패했습니다.\n직원에게 문의해주세요"
        self.set_txt(txt,1)
        self.voice_status_setting(txt,"main")
        btn_control.main_ui_reset(self,MainWindow)

        pass

    sys.exit(0)




def image_numbering():

    global return_hair_location, fontsFolder

    x = 1
    for i in range(4) :
        file_name = "test" + f"{x}"
        target_image = Image.open(f'{return_hair_location}{file_name}.jpg')  #일단 기본배경폼 이미지를 open 합니다.
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

        test.save(f"{return_hair_location}{file_name}.jpg") #편집된 이미지를 저장합니다.

        target_image.close()
        test.close()

def voice_info_img(self,MainWindow):

    txt = f"\
첫 번째 사진입니다. {json_save['content1']}\
두 번째 사진입니다. {json_save['content2']}\
세 번째 사진입니다. {json_save['content3']}\
네 번째 사진입니다. {json_save['content4']}\
미용하실 헤어스타일의 번호를 말씀해 주세요.\
처음으로 돌아가시려면 \"메인화면\" 이라고 말씀해 주세요.\
다시 들으시려면 \"설명해줘\" 라고 말씀해 주세요."
    print(txt)

    self.voice_status_setting(txt,self.window_status)
    pass


def image_choice(self,MainWindow,number):
    global return_hair_location, fontsFolder,photos,image_choice_num

    file_name = "test" + f"{number}"
    target_image = Image.open(f'{return_hair_location}{file_name}.jpg')  #일단 기본배경폼 이미지를 open 합니다.
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

    test.save(f"{return_hair_location}choice.jpg") #편집된 이미지를 저장합니다.

    target_image.close()
    test.close()

    sleep(0.01)

    pixmap = QtGui.QPixmap(f"{return_hair_location}choice.jpg")
    pixmap = pixmap.scaledToWidth(450)
    photos[number-1].setPixmap(QPixmap(pixmap))
    photos[number-1].resize(450,450)
    photos[number-1].show()
    sleep(0.01)

    image_choice_num = number

    text = f"{number}번을 선택하셨습니다. 맞으면 확인, 다르면 취소라 말씀해 주세요."
    self.voice_status_setting(text,"choice_hair")

    btn_control.choice_num_check(self,MainWindow)

def cancel_choice(self,MainWindow):
    global image_choice_num

    pixmap = QtGui.QPixmap(f"{return_hair_location}test{image_choice_num}.jpg")
    pixmap = pixmap.scaledToWidth(450)
    photos[image_choice_num-1].setPixmap(QPixmap(pixmap))
    photos[image_choice_num-1].resize(450,450)
    photos[image_choice_num-1].show()
    sleep(0.01)

    text = f"취소했습니다. 다른 번호를 선택하시거나 기능을 말씀해 주세요."
    self.voice_status_setting(text,"show_hair")
    image_choice_num = 0
    btn_control.end_hair_voice_info(self,MainWindow)

def ckeck_choice(self,MainWindow):
    global image_choice_num,photos
    
    self.face_type.hide()
    self.face_type_value.hide()
    for i in photos:
        i.hide()
        sleep(0.01)

    self.emotion_img.show()

    text = f"미용을 시작하겠습니다.\n미용이 끝나시면 '계산' 혹은 '종료'라고 말씀해 주세요."
    self.set_txt("       미용을 시작하겠습니다.",1)
    self.voice_status_setting(text,"start_hair")
    image_choice_num = 0
    btn_control.start_hair(self,MainWindow)

def emotion_icon(self,MainWindow):
    global emotion
    smile_pixmap = QtGui.QPixmap(f"./font/smile.png")
    smile_pixmap = smile_pixmap.scaledToWidth(100)
    sad_pixmap = QtGui.QPixmap(f"./font/angry.png")
    sad_pixmap = sad_pixmap.scaledToWidth(100)
    while 1:
        if self.window_status!="start_hair":
            pass

        else:
            if  emotion != {}:
                try:
                    if emotion['emotion'] == 'happy':
                        self.emotion_img.setPixmap(QPixmap(smile_pixmap))
                        self.emotion_img.resize(100,100)
                        print("emotion setting")
                        emotion = {}

                    elif emotion['emotion'] == 'angry':
                        self.emotion_img.setPixmap(QPixmap(sad_pixmap))
                        self.emotion_img.resize(100,100)
                        print("emotion setting")
                        emotion = {}

                except:
                    print("emotion setting fail")

        sleep(1)

def end_hair(self,MainWindow):
    text = f"      미용이 종료되었습니다.\n       즐거운 하루 보내세요."
    self.set_txt(text,1)
    self.voice_status_setting(text,"main")

    btn_control.main_page_voice_info(self,MainWindow)
    btn_control.main_ui_reset(self,MainWindow)
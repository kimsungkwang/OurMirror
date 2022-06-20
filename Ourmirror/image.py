from time import sleep

import cv2
import time
from mqtt_client import face_login,emotion_scan

# Explicitly open a new file called my_image.jpg

file_location = "temp/image/"
login_face_location = "temp/login_image/"
emotion_image_location = "temp/emotion_image/"


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


def pi_camera():
    global cap,ret, frame

    print("start camera")


    now = time.localtime()

    ret, frame = cap.read() 
    cap.set(3,640) # 너비
    cap.set(4,480) # 높이
    file_name = f"{file_location}{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}{now.tm_min}{now.tm_sec}.jpg"


    cv2.imwrite(f'{file_name}', frame) # 사진 저장
    print("end camera")




def user_face_scan(self,MainWindow):
    global cap,face_classifier

    i = 0
    text_num = 0
    time_count = 0
    error_count = 0

    if cap.isOpened():
        print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
    else:
        print("No Camera")


    try:

        while True:
            ret, frame = cap.read() 
            if ret and self.video_stop == 0:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 얼굴 검출
                faces = face_classifier.detectMultiScale(gray,1.3,5)
                
                for (x,y,w,h) in faces:
                    if(w>100 and h>100):
                        self.face_scan_enable = 1
                        self.face_scan_timer = 600
                        if(self.window_status=="main"):
                            now = time.localtime()
                            file_name = f"{login_face_location}{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}{now.tm_min}{now.tm_sec}_{i}.jpg"
                            i = i+1
                            if(i>1000):
                                i = 0
                            cv2.imwrite(f'{file_name}', frame)
                            face_login(self,MainWindow)

                        elif(self.window_status=="start_hair"):
                            if time_count>=70:
                                now = time.localtime()
                                file_name = f"{emotion_image_location}{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}{now.tm_min}{now.tm_sec}_{i}.jpg"
                                i = i+1
                                cv2.imwrite(f'{file_name}', frame)
                                emotion_scan(self,MainWindow)
                                time_count = 0
                                if(i>1000):
                                    i = 0

                       

                time_count = time_count +1
                if time_count>5000:
                    time_count = 50
                sleep(0.05)
                #cv2.imshow('video', frame)
                error_count = 0
            else:
                print('video error')
                print(self.video_stop)
                sleep(1)
                error_count = error_count + 1
                if error_count > 10:
                    cap.release()
                    del cap
                    cap = cv2.VideoCapture(0)
                    if cap.isOpened():
                        print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
                    else:
                        print("No Camera")
                    error_count = 0

            
    except:
        print("video end")
        cap.release()
        cv2.destroyAllWindows()


def sys_end():
    global cap

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        user_face_scan()
    except:
        sys_end()
from time import sleep
from gui import btn_control

user_data = {}
now_stats = 0

def user_login(self,MainWindow):
    global now_stats, user_data

    while 1:

        if user_data != {}:
            try:
                if self.user_name != user_data['name']:
                    now_stats = 1
            
                    self.user_name = user_data['name']
                    self.user_phone = user_data['phone']
                    self.user_type = user_data['gender']


                    txt = f"          {self.user_name}님 반갑습니다.\n\
오늘은 어떤 스타일을 하러 오셨나요?"
                    voice = f"{self.user_name}님 반갑습니다. 오늘은 어떤 스타일을 하러 오셨나요?"

                    self.voice_status_setting(voice,self.window_status)
                    self.set_txt(txt,1)
                    self.face_scan_enable = 0
                    user_data = {}
                    pass
            except:
                print("user data error")


        if now_stats == 1 and self.face_scan_timer > 0 :
            if self.video_stop == 0:
                self.face_scan_timer = self.face_scan_timer -1  
        
        elif now_stats == 1 and self.face_scan_timer == 0:
            if self.window_status == "start_hair":
                self.face_scan_timer == 600
            else:    
                self.face_scan_timer = -1
                now_stats = 0
                self.face_scan_enable = 0

                self.user_name = ""
                self.user_phone = ""
                self.user_type = ""
                user_data = {}


                txt = "       자동 로그아웃 되었습니다."

                self.voice_status_setting(txt,self.window_status)
                self.set_txt(txt,1)
                btn_control.main_ui_reset(self,MainWindow)

        #print(f"{now_stats}, {self.face_scan_timer}")
        sleep(0.1)
        

def user_data_setting(data): 
    global user_data

    user_data = data
    #print(user_data)

def status_check():
    global now_stats
    return now_stats
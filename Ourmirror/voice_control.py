#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

from tracemalloc import stop
import speech_recognition as sr
import requests
import json
import io
from gui import facegui, btn_control, trendgui
from pydub import AudioSegment
from pydub.playback import play
import vlc
import sys

rest_api_key = 'fe5f954879fb876ab9d54a91930d274e'
# Record Audio
r = sr.Recognizer()

voice_file = "./temp/voice_file.mp3"
player = vlc.MediaPlayer(voice_file)

cmd_main = ["메인 화면", "초기 화면", "처음으로 돌아가줘", "메일함"]

cmd_facescan = ["얼굴 인식","얼굴 분석","머리 추천", "머리 분석", "헤어스타일 추천", "헤어 추천","추천해 줘"]

cmd_cut = ["커트", "컷", "코트", "커튼", "캡처","커피","커플"]
cmd_perm = ["펌", "퍼머", "파마", "펌으로", "폼으로"]

choice_1 = ["1번", "일본", "일번"]
choice_2 = ["2번", "이본", "이번", "입원"]
choice_3 = ["3번", "삼본", "삼번"]
choice_4 = ["4번", "사본", "사번","카본"]

cmd_voice_info_img = ["설명"]

choice_ckeck = ["확인"]
choice_cancel = ["취소"]

end_hair = ["계산", "종료"]

cmd_trend = ["유행", "우행", "유행하는 머리", "우행하는 머리", "최신 유행"]
cmd_men = ["남성", "남자","삼성"]
cmd_women = ["여성", "여자"]

cmd_show_img = ["사진", "보여줘"]
cmd_voice_retry = ["다시", "말해줘"]

def voice_scan(self,MainWindow):
    while 1:
        with sr.Microphone() as source:
            #print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            txt = r.recognize_google(audio)
            print("You said: " + txt)
            print(self.window_status)

            voice_command(self,MainWindow,txt)

        except:
            pass

def voice_command(self,MainWindow,input_data):
    global cmd_main, cmd_facescan, cmd_cut, cmd_perm, cmd_trend
    global choice_1, choice_2, choice_3, choice_4, cmd_voice_info_img
    global choice_cancel, choice_ckeck, end_hair
    global cmd_trend, cmd_men, cmd_women, cmd_show_img, cmd_voice_retry


    #메인화면 돌아가기   
    if(voice_check(input_data, cmd_main) and self.window_status != "wait"):
        btn_control.main_page_setting(self,MainWindow)
        
    if(self.window_status == "main"):
        #얼굴 분석하기
        if(voice_check(input_data, cmd_facescan)):
            if(self.face_scan_timer > 0):
                facegui.face_scan(self,MainWindow)
            else:
                text = "거울 앞에 아무도 없습니다.\n자리에 앉아서 작동해주세요"
                kakao_voice(text)
                self.set_txt(text,1)

        if(voice_check(input_data, cmd_trend)):
            if(self.face_scan_timer > 0):
                trendgui.start_trend(self,MainWindow)
            else:
                text = "거울 앞에 아무도 없습니다.\n자리에 앉아서 작동해주세요"
                kakao_voice(text)
                self.set_txt(text,1)

    elif(self.window_status == "init_hair"):
        if(voice_check(input_data, cmd_cut)):
            facegui.start_camera(self,MainWindow,"cut")
        if(voice_check(input_data, cmd_perm)):
            facegui.start_camera(self,MainWindow,"perm")

    elif(self.window_status == "show_hair"):
        if(voice_check(input_data, choice_1)):
            facegui.image_choice(self,MainWindow,1)
        elif(voice_check(input_data, choice_2)):
            facegui.image_choice(self,MainWindow,2)
        elif(voice_check(input_data, choice_3)):
            facegui.image_choice(self,MainWindow,3)
        elif(voice_check(input_data, choice_4)):
            facegui.image_choice(self,MainWindow,4)
        elif(voice_check(input_data, cmd_voice_info_img)):
            print("설명")
            facegui.voice_info_img(self,MainWindow)

    elif(self.window_status == "choice_hair"):
        if(voice_check(input_data, choice_ckeck)):
            facegui.ckeck_choice(self,MainWindow)
        elif(voice_check(input_data, choice_cancel)):
            facegui.cancel_choice(self,MainWindow)

    elif(self.window_status == "start_hair"):
        if(voice_check(input_data, end_hair)):
            facegui.end_hair(self,MainWindow)

    elif(self.window_status == "init_trend"):
        if(voice_check(input_data, cmd_cut)):
            trendgui.select_trend(self,MainWindow,"cut")
        elif(voice_check(input_data, cmd_perm)):
            trendgui.select_trend(self,MainWindow,"perm")

    elif(self.window_status == "chart_trend"):
        if(voice_check(input_data, cmd_show_img)):
            print("img show trend")
            trendgui.trend_img_show(self,MainWindow)
        elif(voice_check(input_data, cmd_voice_retry)):
            trendgui.voice_retry(self,MainWindow)

    elif(self.window_status == "img_trend"):
        if(voice_check(input_data, choice_1)):
            trendgui.choice_img(self,MainWindow,1)
        elif(voice_check(input_data, choice_2)):
            trendgui.choice_img(self,MainWindow,2)
        elif(voice_check(input_data, choice_3)):
            trendgui.choice_img(self,MainWindow,3)
        elif(voice_check(input_data, choice_4)):
            trendgui.choice_img(self,MainWindow,4)

    elif(self.window_status == "choice_hair_trend"):
        if(voice_check(input_data, choice_ckeck)):
            facegui.ckeck_choice(self,MainWindow)
        elif(voice_check(input_data, choice_cancel)):
            trendgui.cancel_choice_trend(self,MainWindow)



def voice_check(input_data,cmd):
    for i in cmd:
        val = input_data.find(i)
        if(val != -1):
            return True
    
    return False





#------------------------------------------------
def kakao_voice(data):
    global rest_api_key, player, voice_file
    player.stop()
    del player
    URL = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize" 
    HEADERS = {
    "Content-Type" : "application/xml",
    "Authorization" : "KakaoAK " + rest_api_key,
    }
    DATA = f"""
    <speak>
    {data}
    </speak>
    """
    res = requests.post(URL, headers = HEADERS, data = DATA.encode('utf-8'))
    print(res)
    # 음성 합성 결과를 파일로 저장하기
    with open(voice_file, "wb") as f:
        f.write(res.content)
    player = vlc.MediaPlayer(voice_file)
    player.play()
    


if __name__ == "__main__":
    voice_scan(0,0)
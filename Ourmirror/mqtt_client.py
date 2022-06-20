import paho.mqtt.publish as publish
import time
import os

mqtt_server_ip = "54.150.133.192"
#mqtt_server_ip = "127.0.0.1"

dir_path = "./temp/image"
login_dir_path = "./temp/login_image"
emotion_dir_path = "./temp/emotion_image"

def image_byte(name):
    try:
        f = open(name,"rb")
        fileContent= f.read()
        byteArr = bytearray(fileContent)
        f.close()
        os.remove(name)
        return byteArr

    except Exception as e:
        print("이미지 파일 없음")
        return -1


def image_send(self,MainWindow):
    file_list = os.listdir(dir_path)
    file_list.sort(reverse=True)
    print(file_list)

    directory = f"{self.user_name}_{self.user_phone}"  

    for i in file_list:
        byteArr = image_byte(f"{dir_path}/{i}")
        publish.single(f"{directory}", byteArr, hostname=mqtt_server_ip)
        publish.single(f"bigdata", byteArr, hostname=mqtt_server_ip)
 
def hair_setting_send(self,MainWindow):

    msg = f"init_hair,{self.user_name},{self.user_phone},{self.user_type},{self.user_hair}"
    publish.single("Image", msg, hostname=mqtt_server_ip)
    publish.single(f"bigdata", msg, hostname=mqtt_server_ip)

def face_login(self,MainWindow):
    file_list = os.listdir(login_dir_path)
    file_list.sort(reverse=True)
    print(file_list)

    for i in file_list:
        byteArr = image_byte(f"{login_dir_path}/{i}")
        publish.single(f"login", byteArr, hostname=mqtt_server_ip)

def emotion_scan(self,MainWindow):
    file_list = os.listdir(emotion_dir_path)
    file_list.sort(reverse=True)
    print(file_list)

    for i in file_list:
        byteArr = image_byte(f"{emotion_dir_path}/{i}")
        publish.single(f"emotion", byteArr, hostname=mqtt_server_ip)
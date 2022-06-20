import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from time import sleep
import json
from gui import facegui
import user
from PIL import Image

mqtt_server_ip = '54.150.133.192'
#mqtt_server_ip = "127.0.0.1"


status = 0
photo_num = 1
recv_end = 0

photo_save_location = "./temp/return_image/"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("mirror image client OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    #print("subscribed: " + str(mid) + " " + str(granted_qos))
    pass


def message_type(json_type):
    if json_type['type'] == 'bigdata':
        facegui.json_val_save(json_type)
        print("json recv")
    
    elif json_type['type'] == 'emotion':
        facegui.emotion_recv(json_type)
        print("emotion recv")
    elif json_type['type'] == 'login':
        user.user_data_setting(json_type)
        #print("login recv")
    pass



def on_message(client, userdata, msg):
    global status, photo_num, photo_save_location, recv_end

    
    try:
        check = str(msg.payload.decode("utf-8"))
        print("msg recv")
        try:
            d = json.loads(msg.payload)
            message_type(d)
            
        except:
            print("message error1")
            print("error: "+ check)
            print()

    except:
        if status == 1:
            try:
                f_name = f"{photo_save_location}test{photo_num}.jpg"
                f = open(f_name, "wb")
                f.write(msg.payload)
                print("Image Received")
                f.close()


                # 사이즈 변환
                image = Image.open(f_name)

                weight = 450
                weight_ratio = weight/image.size[0]
                hight = int((float(image.size[1])) *  weight_ratio)


                resize_image = image.resize((weight,hight),Image.ANTIALIAS)

                resize_image.save(f_name)
                resize_image.close()
                image.close()
                


                photo_num = photo_num + 1

                if photo_num>=5 : 
                    photo_num = 1
                    recv_end = 1
            except:
                print("message error2")

    
def recv_status_check(self,MainWindow):
    global status, recv_end, photo_num
    while 1: 
        status = self.mqtt_status
        if recv_end == 1:
            self.mqtt_recv_end = 1
            recv_end = 0
        if status == 0:
            photo_num = 1
        sleep(0.2)





# 새로운 클라이언트 생성

# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# address : localhost, port: 1883 에 연결
try:
    client.connect(mqtt_server_ip, 1883)
    client.subscribe('Mirror', 1)
    client.loop_start()


except:
    print("connect fail")


import cv2


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
else:
    print("No Camera")

i=1
try:
    while True:
        ret, frame = cap.read() 
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 얼굴 검출
            faces = face_classifier.detectMultiScale(gray,1.3,5)

            
            for (x,y,w,h) in faces:
                print(w," ",h)
                print("Test")

                #cv2.imshow('face', cropped_face)
            cv2.imshow('video', frame)

            if cv2.waitKey(1) == 27: break # ESC 키
        else:
            print('error')

except:
    cap.release()
    cv2.destroyAllWindows()
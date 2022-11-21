import cv2
import numpy as np
import os 
from time import sleep
import sys
from socket import *

DEBUG = True
TAS_PORT = 3333
def send_to_TAS(cntName, data):
    send_to_TAS_(cntName, data)
    send_to_TAS_(cntName, data)

def send_to_TAS_(cntName, data):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('127.0.0.1', TAS_PORT))
    if DEBUG:
        print("[*] {}".format((cntName + '/' + data).encode('utf-8')))
    client.send((cntName + '/' + data).encode('utf-8'))
    client.close()


cin = int(sys.argv[1])
def face_recognition():
    os.system("./led 1")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        #os.system("./led 1")
        ret, img =cam.read()
        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                os.system("./led 3")
                sleep(5)
                os.system("./led 4")
                return 1
            else:
                os.system("./led 2")
                sleep(5)
                os.system("./led 4")
                return 0

if __name__ == "__main__":
    if cin == 1:
        out=face_recognition()
        if out==1:
            print("Welcome!")
        else:
            print("Fuck off!")
        send_to_TAS('camera_data', str(out))

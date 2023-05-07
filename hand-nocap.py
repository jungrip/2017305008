import cv2
import sys
import mediapipe as mp
import numpy as np
import math
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))

compare = [[5,4],[6,8],[10,12],[14,16],[18,20]]
open = [False,False,False,False,False]
gesture = [
    [False,False,False,False,False,"Zero"],
    [False,True,False,False,False,"One"],
    [False,True,True,False,False,"Two"],
    [False,True,True,True,False,"Three"],
    [False,True,True,True,True,"Four"],
    [True,True,True,True,True,"Five"]
]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not opened")
    sys.exit(1)

hands = mp_hands.Hands()

while True:
    res, frame = cap.read()

    if not res:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            for i in range(0, 5):
                open[i] = dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                               hand_landmarks.landmark[compare[i][0]].x, hand_landmarks.landmark[compare[i][0]].y) < dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                               hand_landmarks.landmark[compare[i][1]].x, hand_landmarks.landmark[compare[i][1]].y)

            for i in range(0, len(gesture)):
                flag = True
                for j in range(0, 5):
                    if(gesture[i][j] != open[j]):
                        flag = False
                if(flag == True):
                    if(i==5):
                        GPIO.setup(23, GPIO.HIGH)
                        #GPIO.output(18, GPIO.HIGH)
                        #time.sleep(2)
                    elif(i==0):
                        GPIO.setup(23, GPIO.LOW)
                        #GPIO.output(18, GPIO.LOW)
                        #time.sleep(2)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        GPIO.setup(23, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.cleanup()
        break

cap.release()

import cv2
import sys
import mediapipe as mp
import numpy as np
import math
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

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
    h, w, c = frame.shape

    if not res:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            for i in range(0, 5):
                open[i] = dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                               hand_landmarks.landmark[compare[i][0]].x, hand_landmarks.landmark[compare[i][0]].y) < dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                               hand_landmarks.landmark[compare[i][1]].x, hand_landmarks.landmark[compare[i][1]].y)

            text_x = (hand_landmarks.landmark[0].x * w)
            text_y = (hand_landmarks.landmark[0].x * h)
            for i in range(0, len(gesture)):
                flag = True
                for j in range(0, 5):
                    if(gesture[i][j] != open[j]):
                        flag = False
                if(flag == True):
                    cv2.putText(frame, gesture[i][5], (round(text_x), round(text_y) + 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    if(i==5):
                        GPIO.output(17, True)
                        #time.sleep(2)
                    elif(i==0):
                        GPIO.output(17, False)
                        #time.sleep(2)

    cv2.imshow("MediaPipe Hands", frame)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        GPIO.output(17, False)
        GPIO.cleanup()
        break

cv2.destroyAllWindows()
cap.release()

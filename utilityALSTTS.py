#!/usr/bin/env python
# coding: utf-8



import cv2
import pickle
import mediapipe as mp
import numpy as np
from gtts import gTTS
import os
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

with open('ASL_TTS_MDP.pkl', 'rb') as f:
    model = pickle.load(f)
    
class_mapping =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'space', 'del', 'nothing']

def check_prediction(landmarks):
    y_pred=model.predict(landmarks)
    max_indexes = np.argmax(y_pred, axis=1)
    Y_pred=max_indexes
    value= class_mapping[Y_pred[0]]
    return value

def play_text(message):
    language = 'en'
  
    myobj = gTTS(text=message, lang=language, slow=False)

    myobj.save("welcome.mp3")
    os.system("welcome.mp3")    


def open():
    value="  "
    val=""
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands( model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.") # If loading a video, use 'break' instead of 'continue'. continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            flag=0
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                    landmarks_list=[]
                    for landmark in hand_landmarks.landmark:
                        # append the x,y,z values of each landmark point to the array
                        landmarks_list.extend([landmark.x, landmark.y])
                    val=check_prediction(np.asarray([landmarks_list]))
                    print(val)
                    displayText=val
                    if val=="space":
                        #if len(value)==0:
                        value+="Space"
                        play_text(value)
                        print(value)
                        value=" "
                        time.sleep(10)
                    elif val=="del":
                        value=value[:-1]
                    elif value[-1]!=val:
                        value+=val
                        print(value)
                        #time.sleep(10)

                image=cv2.flip(image, 1)    
                cv2.putText(image, displayText, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (200,20,198), 2, cv2.LINE_AA)    
            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'  
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')    
            #Flip the image horizontally for a selfie-view display.
            # cv2.imshow('MediaPipe Hands',image )
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break
    cap.release()







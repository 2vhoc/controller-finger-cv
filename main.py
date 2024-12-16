import cv2, os, pyautogui
import mediapipe as mp
import time
from math import *

postionStart = 0
postionEnd = 0
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.55, min_tracking_confidence=0.5)
mpDrawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920/3) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080/3) 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    posHands = []
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame = cv2.flip(frame, -1)
    frame = cv2.flip(frame, 1)
    
    
    


    results = hands.process(frame)
    allHands = []
    

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mpDrawing.draw_landmarks(frame, landmarks, mpHands.HAND_CONNECTIONS)
            x, y = None, None
            posHands = [] 
            for id, landmark in enumerate(landmarks.landmark):
                h, w, c = frame.shape 
                x, y = int((landmark.x) * w), int(landmark.y * h)  
                posHands.append([id, x, y])

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(frame, str(f'{id}'), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            allHands.append(posHands)


        if len(allHands) > 0:
                pyautogui.moveTo(allHands[0][8][1] * 3, allHands[0][8][2] * 3, 0, pyautogui.easeInOutQuad)
                postionStart = allHands[0][8][1]
                if abs(allHands[0][8][1] - allHands[0][4][1] < 10):
                    pyautogui.click()
                    pass
                
                elif allHands[0][20][2] >= allHands[0][17][2] and abs(postionEnd - postionStart) >= 5:
                    pyautogui.scroll(postionStart - postionEnd)
                postionEnd = postionStart
                    
        

    cv2.imshow("Hand Detection", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

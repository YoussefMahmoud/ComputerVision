import mediapipe as mp
import cv2
import time
import numpy as np
import math
import pyautogui
from win_func import Volume
from hand_gestures import Hands


vol=Volume()

########################################

mp_draw = mp.solutions.drawing_utils

#setting the used camera, if you are not using your main camera change the number to 1 or 2
cap = cv2.VideoCapture(0)

green = mp_draw.DrawingSpec((0, 255, 0), 1, 1)


with mp.solutions.Holistic() as holistic:
    while cap.isOpened():
        #configuring the video feed
        success, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        rLandmarks = results.right_hand_landmarks.landmark
        lLandmarks = results.left_hand_landmarks.landmark
        hands = Hands(rLandmarks, lLandmarks)

        #visualising hands landmarks
        mp_draw.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.HAND_CONNECTIONS)

        try:
            rLandmarks = results.right_hand_landmarks.landmark
            detection = "Detected"

            #configuring the needed fingers
            rThumpTip_xy = hands.get_xy(rThumpTip)
            cv2.circle(image, rThumpTip_xy, 5, white, cv2.FILLED)

            rIndexTip = rLandmarks[mp.solutions.HandLandmark.INDEX_FINGER_TIP].x, rLandmarks[
                mp.solutions.HandLandmark.INDEX_FINGER_TIP].y
            rIndexTip_xy = hands.get_xy(rIndexTip)
            cv2.circle(image, rIndexTip_xy, 5, white, cv2.FILLED)

            rPinkyTip = rLandmarks[mp.solutions.HandLandmark.PINKY_TIP].x, rLandmarks[
                mp.solutions.HandLandmark.PINKY_TIP].y
            rPinkyTip_xy = hands.get_xy(rPinkyTip)
            cv2.circle(image, rPinkyTip_xy, 5, white, cv2.FILLED)

            rMiddle1 = rLandmarks[mp.solutions.HandLandmark.MIDDLE_FINGER_MCP].x, rLandmarks[
                mp.solutions.HandLandmark.MIDDLE_FINGER_MCP].y

            rMiddle2 = rLandmarks[mp.solutions.HandLandmark.MIDDLE_FINGER_PIP].x, rLandmarks[
                mp.solutions.HandLandmark.MIDDLE_FINGER_PIP].y
            rMiddle2_xy = hands.get_xy(rMiddle2)

            rMiddle3 = rLandmarks[mp.solutions.HandLandmark.MIDDLE_FINGER_DIP].x, rLandmarks[
                mp.solutions.HandLandmark.MIDDLE_FINGER_DIP].y

            #finding the angle between the knuckles of the middle finger
            volume_angle = hands.get_angle(rMiddle1, rMiddle2, rMiddle3)
            #finding the distance between the thump and the other fingers
            volume_i_length = hands.get_length(rIndexTip_xy, rThumpTip_xy)
            volume_d_length = hands.get_length(rPinkyTip_xy, rThumpTip_xy)

            #increasing the volume
            if volume_i_length > 50:
                finger_length = "Far"
            if volume_i_length < 30 and finger_length == "Far":
                finger_length = "Not Far"
                vol.volume_up()
                # pyautogui.press('up')
                print('Volume up')


            #decreasing the volume
            if volume_d_length > 50:
                pinky_finger_length = "Far"
            if volume_d_length < 30 and pinky_finger_length == "Far":
                pinky_finger_length = "Not Far"
                print('Fingers Touching')
                vol.volume_down()
                # pyautogui.press('down')
                print('Volume down')


            #pausing/playing
            if volume_angle > 100:
                hand_state = "Open"
            if volume_angle < 30 and hand_state == "Open":
                hand_state = "Closed"
                #if it doesn't work well on linux change to 
                #pyautogui.press('space')
                pyautogui.press('playpause')
                print('Play/Pause')

        except:
            pass
        
        #showing volume level on the top left side of the feed
        cv2.putText(image, str(vol.get_volume()), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, black)
        #cv2.putText(image, str(hand_state), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, black)

        cv2.imshow('Frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
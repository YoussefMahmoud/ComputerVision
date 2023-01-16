import mediapipe as mp
import cv2
import time
import numpy as np
import math
import pyautogui
#for windows #from win_func import Volume#
from linux_func import Volume
########################################
white = (255, 255, 255)
black = (0, 0, 0)
blue = (255, 0, 0)
red = (0, 0, 255)

detection = None
finger_length = None
pinky_finger_length = None
hand_state = None
vol = 0
########################################

mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

#setting the used camera, if you are not using your main camera change the number to 1 or 2
cap = cv2.VideoCapture(0)

green = mp_draw.DrawingSpec((0, 255, 0), 1, 1)

#converting radians to angles
def get_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[0] - b[0], c[1] - b[1]) - np.arctan2(a[0] - b[0], a[1] - b[1])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

#getting the space between fingers
def get_length(a, b):
    a = np.array(a)
    b = np.array(b)

    length = math.hypot(a[0] - b[0], a[1] - b[1])
    return length

#getting the position a finger on the screen
def get_xy(point):
    xy = tuple(np.multiply(point, [640, 480]).astype(int))
    return xy



with mp_holistic.Holistic() as holistic:
    while cap.isOpened():
        #configuring the video feed
        success, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #visualising hands landmarks
        mp_draw.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        try:
            rLandmarks = results.right_hand_landmarks.landmark
            detection = "Detected"

            #configuring the needed fingers
            rThumpTip = rLandmarks[mp_holistic.HandLandmark.THUMB_TIP].x, rLandmarks[
                mp_holistic.HandLandmark.THUMB_TIP].y
            rThumpTip_xy = get_xy(rThumpTip)
            cv2.circle(image, rThumpTip_xy, 5, white, cv2.FILLED)

            rIndexTip = rLandmarks[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x, rLandmarks[
                mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
            rIndexTip_xy = get_xy(rIndexTip)
            cv2.circle(image, rIndexTip_xy, 5, white, cv2.FILLED)

            rPinkyTip = rLandmarks[mp_holistic.HandLandmark.PINKY_TIP].x, rLandmarks[
                mp_holistic.HandLandmark.PINKY_TIP].y
            rPinkyTip_xy = get_xy(rPinkyTip)
            cv2.circle(image, rPinkyTip_xy, 5, white, cv2.FILLED)

            rMiddle1 = rLandmarks[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x, rLandmarks[
                mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y

            rMiddle2 = rLandmarks[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].x, rLandmarks[
                mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            rMiddle2_xy = get_xy(rMiddle2)

            rMiddle3 = rLandmarks[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].x, rLandmarks[
                mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y

            #finding the angle between the knuckles of the middle finger
            volume_angle = get_angle(rMiddle1, rMiddle2, rMiddle3)
            #finding the distance between the thump and the other fingers
            volume_i_length = get_length(rIndexTip_xy, rThumpTip_xy)
            volume_d_length = get_length(rPinkyTip_xy, rThumpTip_xy)

            #increasing the volume
            if volume_i_length > 50:
                finger_length = "Far"
            if volume_i_length < 30 and finger_length == "Far":
                finger_length = "Not Far"
                Volume.volume_up()

            #decreasing the volume
            if volume_d_length > 50:
                pinky_finger_length = "Far"
            if volume_d_length < 30 and pinky_finger_length == "Far":
                pinky_finger_length = "Not Far"
                Volume.volume_down()

            #pausing/playing
            if volume_angle > 100:
                hand_state = "Open"
            if volume_angle < 30 and hand_state == "Open":
                hand_state = "Closed"
                #if it doesn't work well on linux change to 
                #pyautogui.press('space')
                pyautogui.press('playpause')

        except:
            pass
        
        #showing volume level on the top left side of the feed
        cv2.putText(image, str(Volume.volume()), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, black)
        cv2.imshow('Frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
from hand_gestures import Hands
import keyboard
import pyautogui

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        
        try:
            rLandmarks = results.right_hand_landmarks.landmark if results.right_hand_landmarks else None
            lLandmarks = results.left_hand_landmarks.landmark if results.left_hand_landmarks else None
            
            # Create hands object with whatever landmarks are available
            hands = Hands(rLandmarks, lLandmarks)

            # Test right hand if it exists
            if hands.rMiddle:
                test = Hands.hand_closed(*hands.rMiddle)
                if test == True:
                    print('Right Hand Closed')

            
            # Test left hand if it exists
            if hands.lMiddle:
                test2 = Hands.hand_closed(*hands.lMiddle)
                if test2 == True:
                    print('Left Hand Closed')
        except Exception as e:
            pass
        
        cv2.imshow('Feed', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
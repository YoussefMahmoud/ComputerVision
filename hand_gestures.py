import numpy as np
import math
import mediapipe as mp
import cv2

class Hands:
    def __init__(self, rLandmarks=None, lLandmarks=None):
        # --- Right Hand Tips ---
        if rLandmarks:
            self.rThumbTip = (
                rLandmarks[mp.solutions.holistic.HandLandmark.THUMB_TIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.THUMB_TIP].y
            )
            self.rIndexTip = (
                rLandmarks[mp.solutions.holistic.HandLandmark.INDEX_FINGER_TIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.INDEX_FINGER_TIP].y
            )
            self.rMiddleTip = (
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_TIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_TIP].y
            )
            self.rRingTip = (
                rLandmarks[mp.solutions.holistic.HandLandmark.RING_FINGER_TIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.RING_FINGER_TIP].y
            )
            self.rPinkyTip = (
                rLandmarks[mp.solutions.holistic.HandLandmark.PINKY_TIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.PINKY_TIP].y
            )

            # --- Right Middle Finger (MCP, PIP, DIP) ---
            self.rMiddle1 = (
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_MCP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_MCP].y
            )
            self.rMiddle2 = (
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_PIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            )
            self.rMiddle3 = (
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_DIP].x,
                rLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_DIP].y
            )
            
            self.rMiddle = (self.rMiddle1, self.rMiddle2, self.rMiddle3)
        else:
            self.rThumbTip = None
            self.rIndexTip = None
            self.rMiddleTip = None
            self.rRingTip = None
            self.rPinkyTip = None
            self.rMiddle1 = None
            self.rMiddle2 = None
            self.rMiddle3 = None
            self.rMiddle = None

        # --- Left Hand Tips ---
        if lLandmarks:
            self.lThumbTip = (
                lLandmarks[mp.solutions.holistic.HandLandmark.THUMB_TIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.THUMB_TIP].y
            )
            self.lIndexTip = (
                lLandmarks[mp.solutions.holistic.HandLandmark.INDEX_FINGER_TIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.INDEX_FINGER_TIP].y
            )
            self.lMiddleTip = (
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_TIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_TIP].y
            )
            self.lRingTip = (
                lLandmarks[mp.solutions.holistic.HandLandmark.RING_FINGER_TIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.RING_FINGER_TIP].y
            )
            self.lPinkyTip = (
                lLandmarks[mp.solutions.holistic.HandLandmark.PINKY_TIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.PINKY_TIP].y
            )

            # --- Left Middle Finger (MCP, PIP, DIP) ---
            self.lMiddle1 = (
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_MCP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_MCP].y
            )
            self.lMiddle2 = (
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_PIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            )
            self.lMiddle3 = (
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_DIP].x,
                lLandmarks[mp.solutions.holistic.HandLandmark.MIDDLE_FINGER_DIP].y
            )
            
            self.lMiddle = (self.lMiddle1, self.lMiddle2, self.lMiddle3)
        else:
            self.lThumbTip = None
            self.lIndexTip = None
            self.lMiddleTip = None
            self.lRingTip = None
            self.lPinkyTip = None
            self.lMiddle1 = None
            self.lMiddle2 = None
            self.lMiddle3 = None
            self.lMiddle = None
        
        self.rHand_state = None
        self.lHand_state = None
        
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (255, 0, 0)
        self.red = (0, 0, 255)

    # --- Utility methods ---
    @staticmethod
    def get_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[0] - b[0], c[1] - b[1]) - np.arctan2(a[0] - b[0], a[1] - b[1])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    @staticmethod
    def get_length(a, b):
        a = np.array(a)
        b = np.array(b)
        return math.hypot(a[0] - b[0], a[1] - b[1])

    @staticmethod
    def get_xy(point):
        xy = tuple(np.multiply(point, [640, 480]).astype(int))
        return xy
    
    @staticmethod
    def hand_closed(a, b, c): 
        angle = Hands.get_angle(a, b, c)
        if angle > 100:
            Hands.rHand_state = "open"
            return False
        if angle < 40 and Hands.rHand_state == 'open':
            Hands.rHand_state = 'closed'
            return True
    ##not working
    @staticmethod
    def add_text_to_feed(feed, text, position=(10, 60), text_color=(0,0,0)): 
        cv2.putText(feed, str(text), position, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color)
        
 
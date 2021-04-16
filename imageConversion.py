import numpy as np
import cv2

class imageConverter():
    def __init__(self):
        self.frame = 0

    def get(self):
        return self.frame

    def update(self, frame):
        lower = np.array([42,24,146])
        upper = np.array([128,255,255])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        self.frame = cv2.bitwise_and(frame,frame, mask=mask)
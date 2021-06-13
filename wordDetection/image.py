import cv2
from wordDetection.paperDetection import paperDetection

class image():
    def __init__(self):
        self.paperDetection = paperDetection()

    def cameraDetection(self, cap):
        timer = 0
        word = False
        while (True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, -1)
            word = self.paperDetection.detect(frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if word is not False or timer >= 150:
                return word

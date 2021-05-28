import cv2


class PaperDetection:
    def __init__(self):
        self.frame = 0

    def get(self):
        return self.frame

    def update(self, frame):
        ret, firstThreshold = cv2.threshold(frame, 136, 255, cv2.THRESH_TOZERO)
        edged = cv2.cvtColor(firstThreshold, cv2.COLOR_BGR2GRAY)
        ret, secondThreshold = cv2.threshold(edged, 235, 255, cv2.THRESH_TOZERO_INV)
        ret, thirdThreshold = cv2.threshold(secondThreshold, 100, 255, cv2.THRESH_BINARY)

        contours, h = cv2.findContours(thirdThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get the contours of the white paper on the cardboard and display that back
        xCoordinates = 1
        yCoordinates = 1
        wCoordinates = 1
        hCoordinates = 1
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 100 and h > 100:
                size = cv2.contourArea(cnt)
                if size > 100000:
                    # Debug purposes
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 215, 255), 2)
                    xCoordinates = x
                    yCoordinates = y
                    wCoordinates = w
                    hCoordinates = h
                    break
        self.frame = frame[yCoordinates:yCoordinates + hCoordinates, xCoordinates:xCoordinates + wCoordinates]
        cv2.imshow('test', self.frame)

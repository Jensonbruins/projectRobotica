import cv2
import numpy as np
import math

class lineExtractor():
    def __init__(self):
        self.averageArray = []
        self.previousLastNumber = 0

    def get(self):
        return self.averageArray

    def clean(self):
        self.averageArray = []

    def update(self,letterArray, detectedPaper):
        for index, x in enumerate(letterArray):
            # edit frames to make letters more clear
            temporaryFrame = detectedPaper[x[3]:x[1], x[0]:x[2]]
            blur = cv2.medianBlur(temporaryFrame, 5)
            # blur = cv2.bilateralFilter(temporaryFrame,5,75,75)
            cannyFrame = cv2.Canny(blur, 200, 255)
            # important for cleanup
            # lastNumber = index

            # Check for lines in image
            lines = cv2.HoughLinesP(cannyFrame, 1, np.pi / 180, 11, minLineLength=7, maxLineGap=4)
            # if there are lines in image
            if lines is not None:
                horizontal = 0
                vertical = 0
                diagonal = 0
                # loop over every line in image
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = math.atan2(y1 - y2, x1 - x2)
                    angle = angle * 180 / math.pi
                    if 85 < angle < 95:
                        vertical = vertical + 1
                        cv2.line(temporaryFrame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    elif 175 < angle < 185:
                        horizontal = horizontal + 1
                        cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    elif 100 < angle < 170 or -100 > angle > -170:
                        diagonal = diagonal + 1
                        cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                if len(self.averageArray) >= (index + 1):
                    oldIndex = self.averageArray[index][0]
                    oldHorizontal = self.averageArray[index][1]
                    oldVertical = self.averageArray[index][2]
                    oldDiagonal = self.averageArray[index][3]
                    self.averageArray.pop(index)
                    self.averageArray.insert(index, [(oldIndex + 1), (oldHorizontal + horizontal), (oldVertical + vertical),
                                                (oldDiagonal + diagonal)])
                else:
                    self.averageArray.insert(index, [0, horizontal, vertical, diagonal])

# DEBUG CODE
            cv2.imshow('t' + str(index), temporaryFrame)
#             cv2.imshow('a' + str(index), blur)
#             cv2.imshow('c' + str(index), cannyFrame)
#
        for x in range(len(letterArray), self.previousLastNumber):
            cv2.destroyWindow('t' + str(x))
#             cv2.destroyWindow('a'+str(x))
#             cv2.destroyWindow('c'+str(x))

        self.previousLastNumber = len(letterArray)
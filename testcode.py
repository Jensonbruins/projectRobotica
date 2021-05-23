import cv2
import numpy as np
import math
from paperDetection import paperDetection
from letterDetection import letterDetection

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

#
# TODO: Find a fix for global variable 'previousLastNumber'
#
previousLastNumber = 0
avgIndex = 0
avgHorizontal = 0
avgVertical = 0
avgDiagonal = 0
avgArray = []
avgArrayIndex = 0

paper = paperDetection()
letter = letterDetection()
while(True):
    ret, frame = cap.read()

    paper.update(frame)
    cv2.imshow('test', paper.get())

    letter.update(paper.get())

    #
    # Creating the images of the detected letters

    lastNumber = 0
    for index,x in enumerate(letter.get()):
        temporaryFrame = paper.get()[x[3]:x[1], x[0]:x[2]]
        # blur = cv2.GaussianBlur(temporaryFrame,(5,5),0)
        blur = cv2.medianBlur(temporaryFrame,5)
        blur = cv2.bilateralFilter(blur,9,75,75)
        cannyFrame = cv2.Canny(blur,200,255)
        lastNumber = index

        # edged = cv2.cvtColor(temporaryFrame, cv2.COLOR_BGR2GRAY)
        # print(type(temporaryFrame))
        # temporaryFrame = np.CV_8UC1(temporaryFrame)
        lines = cv2.HoughLinesP(cannyFrame, 1, np.pi / 180, 9, minLineLength=5, maxLineGap=5)
        if lines is not None:
            amountofLines = 0
            print('Image: ',index)
            horizontal = 0
            vertical = 0
            diagonal = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = math.atan2(y1 - y2, x1 - x2)
                angle = angle * 180 / math.pi
                if angle > 85 and angle < 95:
                    vertical = vertical + 1
                    cv2.line(temporaryFrame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                elif angle > 175 and angle < 185:
                    horizontal = horizontal + 1
                    cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                elif angle > 130 and angle < 140 or angle < -130 and angle > -140:
                    diagonal = diagonal + 1
                    cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            #
            # print('Total horizontal lines: ',horizontal)
            # print('Total vertical lines: ',vertical)
            # print('Total diagonal lines: ',diagonal)
            # print('Total amount of lines:',len(lines))
            #
            if avgIndex != 20 and index == 0:
                avgHorizontal = avgHorizontal + horizontal
                avgDiagonal = avgDiagonal + diagonal
                avgVertical = avgVertical + vertical
                avgIndex = avgIndex + 1
            elif avgIndex == 20:
                print('index:', avgIndex)
                print('Average horizontal lines: ',avgHorizontal / 20)
                print('Average vertical lines: ',avgVertical / 20)
                print('Average diagonal lines: ',avgDiagonal / 20)
                avgArray.insert(avgArrayIndex,[avgHorizontal / 20,avgVertical / 20,avgDiagonal / 20])
                avgArrayIndex = avgArrayIndex + 1
                avgIndex = 0
                avgHorizontal = 0
                avgVertical = 0
                avgDiagonal = 0

        cv2.imshow('t'+str(index), temporaryFrame)
        cv2.imshow('a'+str(index), blur)
        cv2.imshow('c'+str(index), cannyFrame)


    #
    # Removing the remaining windows (falsely detected or smaller word)
    #
    for x in range(lastNumber + 1, previousLastNumber + 1):
        cv2.destroyWindow('t'+str(x))
        cv2.destroyWindow('a'+str(x))
        cv2.destroyWindow('c'+str(x))


    previousLastNumber = lastNumber

    #
    # NOTE: Disable properly (20ms wait for better performance)
    #
    if cv2.waitKey(20) & 0xFF == ord('q'):
        print(avgArray)
        break

#
# When everything done, release the capture
#
cap.release()
cv2.destroyAllWindows()
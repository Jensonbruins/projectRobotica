import cv2
import numpy as np
import math
from paperDetection import paperDetection
from letterDetection import letterDetection

cap = cv2.VideoCapture(0)

#
# TODO: Find a fix for global variable 'previousLastNumber'
#
previousLastNumber = 0

paper = paperDetection()
letter = letterDetection()
averageArray = []
while(True):
    ret, frame = cap.read()

    paper.update(frame)
    cv2.imshow('test', paper.get())

    letter.update(paper.get())

    #
    # Creating the images of the detected letters

    lastNumber = 0
    twodarray = []
    # loop over every letter
    for index,x in enumerate(letter.get()):
        # edit frames to make letters more clear
        temporaryFrame = paper.get()[x[3]:x[1], x[0]:x[2]]
        blur = cv2.medianBlur(temporaryFrame,5)
        blur = cv2.bilateralFilter(blur,9,75,75)
        cannyFrame = cv2.Canny(blur,200,255)
        # important for cleanup
        lastNumber = index

        # Check for lines in image
        lines = cv2.HoughLinesP(cannyFrame, 1, np.pi / 180, 9, minLineLength=5, maxLineGap=5)
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

            if len(averageArray) >= (index + 1):
                oldIndex = averageArray[index][0]
                oldHorizontal = averageArray[index][1]
                oldVertical = averageArray[index][2]
                oldDiagonal = averageArray[index][3]
                averageArray.pop(index)
                averageArray.insert(index, [(oldIndex + 1), (oldHorizontal + horizontal), (oldVertical + vertical), (oldDiagonal + diagonal)])
            else:
                averageArray.insert(index, [0, horizontal, vertical, diagonal])

        cv2.imshow('t' + str(index), temporaryFrame)
        # cv2.imshow('a' + str(index), blur)
        # cv2.imshow('c' + str(index), cannyFrame)

    for x in averageArray:
        if x[0] == 20:
            print(averageArray)
            for a in averageArray:
                if a[0] != 0:
                    print('Horizontal: ', a[1]/a[0], 'Vertical: ', a[2]/a[0], 'Diagonal: ', a[3]/a[0])
            averageArray = []
            break


    #
    # Removing the remaining windows (falsely detected or smaller word)
    #
    for x in range(lastNumber + 1, previousLastNumber + 1):
        cv2.destroyWindow('t'+str(x))
        # cv2.destroyWindow('a'+str(x))
        # cv2.destroyWindow('c'+str(x))

    previousLastNumber = lastNumber

    #
    # NOTE: Disable properly (20ms wait for better performance)
    #
    if cv2.waitKey(20) & 0xFF == ord('q'):

        break

#
# When everything done, release the capture
#
cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import math
from paperDetection import paperDetection
from letterDetection import letterDetection

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('control')

cv2.createTrackbar('minLineLength','control',0,255,nothing)
cv2.setTrackbarPos('minLineLength', 'control', 7)
cv2.createTrackbar('maxLineGap','control',0,255,nothing)
cv2.setTrackbarPos('maxLineGap', 'control', 4)
cv2.createTrackbar('threshold','control',0,255,nothing)
cv2.setTrackbarPos('threshold', 'control', 11)
#
# TODO: Find a fix for global variable 'previousLastNumber'
#
previousLastNumber = 0

paper = paperDetection()
letter = letterDetection()
averageArray = []
while(True):
    letterArray = [
    #   ['letter', horizontalMin, horizontalMax, verticalMin, verticalMax, diagonalMin, diagonalMax]
        ['A', 1, 2, 0, 0.2, 7.5, 9.1],
        ['B', 5.5, 6.5, 4.5, 7, 2, 3],
        ['C', 0, 0, 0, 0, 0, 0],
        ['D', 3, 4.5, 3.5, 5.5, 2.5, 4],
        ['E', 5.5, 7.5, 1.5, 3.5, 0, 0.5],
        # ['F', 0, 0, 0, 0, 0, 0],
        # ['G', 0, 0, 0, 0, 0, 0],
        # ['H', 0, 0, 0, 0, 0, 0],
        # ['I', 0, 0, 0, 0, 0, 0],
        # ['J', 0, 0, 0, 0, 0, 0],
        # ['K', 0, 0, 0, 0, 0, 0],
        # ['L', 0, 0, 0, 0, 0, 0],
        # ['M', 0, 0, 0, 0, 0, 0],
        ['N', 0, 0.5, 4, 6.5, 4, 5.5],
        # ['O', 0, 0, 0, 0, 0, 0],
        # ['P', 0, 0, 0, 0, 0, 0],
        # ['Q', 0, 0, 0, 0, 0, 0],
        # ['R', 0, 0, 0, 0, 0, 0],
        # ['S', 0, 0, 0, 0, 0, 0],
        # ['T', 0, 0, 0, 0, 0, 0],
        # ['U', 0, 0, 0, 0, 0, 0],
        # ['V', 0, 0, 0, 0, 0, 0],
        # ['W', 0, 0, 0, 0, 0, 0],
        # ['X', 0, 0, 0, 0, 0, 0],
        # ['Y', 0, 0, 0, 0, 0, 0],
        # ['Z', 0, 0, 0, 0, 0, 0],
    ]


    ret, frame = cap.read()

    paper.update(frame)
    cv2.imshow('test', paper.get())

    letter.update(paper.get())

    #
    # Creating the images of the detected letters

    minLineLengthVar = cv2.getTrackbarPos('minLineLength','control')
    maxLineGapVar = cv2.getTrackbarPos('maxLineGap','control')
    thresholdVar = cv2.getTrackbarPos('threshold','control')

    lastNumber = 0
    # loop over every letter
    for index,x in enumerate(letter.get()):
        # edit frames to make letters more clear
        temporaryFrame = paper.get()[x[3]:x[1], x[0]:x[2]]
        blur = cv2.medianBlur(temporaryFrame,5)
        # blur = cv2.bilateralFilter(temporaryFrame,5,75,75)
        cannyFrame = cv2.Canny(blur,200,255)
        # important for cleanup
        lastNumber = index

        # Check for lines in image
        lines = cv2.HoughLinesP(cannyFrame, 1, np.pi / 180, thresholdVar, minLineLength=minLineLengthVar, maxLineGap=maxLineGapVar)
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
        if x[0] == 10:
            # print(averageArray)
            newAverageArray = averageArray
            averageArray = []
            print(' ')
            for a in newAverageArray:
                if a[0] > 5:
                    horizontalAvg = a[1]/a[0]
                    verticalAvg = a[2]/a[0]
                    diagonalAvg = a[3]/a[0]
                    print('Horizontal: ', horizontalAvg, 'Vertical: ', verticalAvg, 'Diagonal: ', diagonalAvg)

                    for l in letterArray:
                        # print(l[0])
                        # print(l[1], horizontalAvg, l[2])
                        if l[1] <= horizontalAvg <= l[2]:
                            # print('worked')
                            # print(l[3], verticalAvg, l[4])
                            if l[3] <= verticalAvg <= l[4]:
                                # print('worked1')
                                if l[5] <= diagonalAvg <= l[6]:
                                    print('target = ', l[0])
                                    break;
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
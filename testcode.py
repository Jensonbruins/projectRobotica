import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('control')

cv2.createTrackbar('firstthreshHoldMin','control',0,255,nothing)
cv2.createTrackbar('firstthreshHoldMax','control',0,255,nothing)
cv2.setTrackbarPos('firstthreshHoldMin', 'control', 136)
cv2.setTrackbarPos('firstthreshHoldMax', 'control', 255)

cv2.createTrackbar('secondthreshHoldMin','control',0,255,nothing)
cv2.createTrackbar('secondthreshHoldMax','control',0,255,nothing)
cv2.setTrackbarPos('secondthreshHoldMin', 'control', 235)
cv2.setTrackbarPos('secondthreshHoldMax', 'control', 255)

cv2.createTrackbar('thirdthreshHoldMin','control',0,255,nothing)
cv2.createTrackbar('thirdthreshHoldMax','control',0,255,nothing)
cv2.setTrackbarPos('thirdthreshHoldMin', 'control', 100)
cv2.setTrackbarPos('thirdthreshHoldMax', 'control', 255)

cv2.createTrackbar('fourththreshHoldMin','control',0,255,nothing)
cv2.createTrackbar('fourththreshHoldMax','control',0,255,nothing)
cv2.setTrackbarPos('fourththreshHoldMin', 'control', 100)
cv2.setTrackbarPos('fourththreshHoldMax', 'control', 255)

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
while(True):
    ret, frame = cap.read()

    # NOTE: Creating a cropped frame (taking out the A4 paper from the picture)
    firstthreshHoldMin = cv2.getTrackbarPos('firstthreshHoldMin', 'control')
    firstthreshHoldMax = cv2.getTrackbarPos('firstthreshHoldMax', 'control')

    secondthreshHoldMin = cv2.getTrackbarPos('secondthreshHoldMin', 'control')
    secondthreshHoldMax = cv2.getTrackbarPos('secondthreshHoldMax', 'control')

    thirdthreshHoldMin = cv2.getTrackbarPos('thirdthreshHoldMin', 'control')
    thirdthreshHoldMax = cv2.getTrackbarPos('thirdthreshHoldMax', 'control')

    ret, firstThreshold = cv2.threshold(frame, firstthreshHoldMin, firstthreshHoldMax, cv2.THRESH_TOZERO)
    edged = cv2.cvtColor(firstThreshold, cv2.COLOR_BGR2GRAY)
    ret, secondThreshold = cv2.threshold(edged, secondthreshHoldMin, secondthreshHoldMax, cv2.THRESH_TOZERO_INV)
    ret, thirdThreshold = cv2.threshold(secondThreshold, thirdthreshHoldMin, thirdthreshHoldMax, cv2.THRESH_BINARY)

    contours, h = cv2.findContours(thirdThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 100 and h > 100:

            # ADDED SIZE CRITERION TO REMOVE NOISES
            size = cv2.contourArea(cnt)
            # print(size)
            if size > 100000:
                # Debug purposes
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 215, 255), 2)
                break
    # cv2.imshow('test', frame)

    croppedFrame = frame[y:y+h, x:x+w]

    #
    # NOTE: Detection of letters
    #
    fourththreshHoldMin = cv2.getTrackbarPos('fourththreshHoldMin', 'control')
    fourththreshHoldMax = cv2.getTrackbarqPos('fourththreshHoldMax', 'control')

    ret, croppedFrameThreshold = cv2.threshold(croppedFrame, fourththreshHoldMin, fourththreshHoldMax, cv2.THRESH_BINARY_INV)
    edged = cv2.cvtColor(croppedFrameThreshold, cv2.COLOR_BGR2GRAY)

    if croppedFrame.size > 100000:
        array = []
        i = 0
        newContours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for index,cnt in enumerate(newContours):
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 25 and w < 70 and h > 25 and h < 70:

                size = cv2.contourArea(cnt)
                if size < 3000:
                    north = x - 5
                    east = (y + h) + 5
                    south = (x + w) + 5
                    west = y - 5
                    if north < 0:
                        north = 0
                    if east < 0:
                        east = 0
                    if south < 0:
                        south = 0
                    if west < 0:
                        west = 0
                    array.insert(i,[north,east,south,west])
                    # cv2.rectangle(croppedFrame, (north, west), (south, east), (0, 215, 255), 2)
                    i = i + 1
        # cv2.imshow('test', croppedFrame)

        #
        # Creating the images of the detected letters

        lastNumber = 0
        for index,x in enumerate(array):
            temporaryFrame = croppedFrame[x[3]:x[1], x[0]:x[2]]
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
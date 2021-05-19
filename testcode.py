import cv2
import numpy as np

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
previousLastNumber = 0
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

    croppedFrame = frame[y:y+h, x:x+w]


    #
    # NOTE: Detection of letters
    #
    fourththreshHoldMin = cv2.getTrackbarPos('fourththreshHoldMin', 'control')
    fourththreshHoldMax = cv2.getTrackbarPos('fourththreshHoldMax', 'control')

    ret, croppedFrameThreshold = cv2.threshold(croppedFrame, fourththreshHoldMin, fourththreshHoldMax, cv2.THRESH_BINARY_INV)
    edged = cv2.cvtColor(croppedFrameThreshold, cv2.COLOR_BGR2GRAY)

    if croppedFrame.size > 100000:
        array = []
        i = 0
        newContours, h = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in newContours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 20 and w < 60 and h > 20 and h < 60:

                size = cv2.contourArea(cnt)
                if size < 1000:
                    array.insert(i,[x,y,w,h])
                    # cv2.rectangle(croppedFrame, (x, y), (x + w, y + h), (0, 215, 255), 2)
                    i = i + 1

        #
        # Creating the images of the detected letters
        #
        lastNumber = 0
        for index,x in enumerate(array):
            cv2.imshow(str(index), croppedFrame[x[1]:x[1]+x[3], x[0]:x[0]+x[2]])
            lastNumber = index

            # TODO: Fix crash on houghlines
            # lines = cv2.HoughLinesP(test, 1, np.pi / 180, 30, maxLineGap=250)
            # for line in lines:
            #     x1, y1, x2, y2 = line[0]
            #     cv2.line(croppedFrame, (x1, y1), (x2, y2), (0, 0, 128), 1)

        #
        # Removing the remaining windows (falsely detected or smaller word)
        #
        for x in range(lastNumber + 1, previousLastNumber + 1):
            cv2.destroyWindow(str(x))
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
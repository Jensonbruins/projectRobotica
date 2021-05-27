import cv2
import numpy as np
import math
from paperDetection import paperDetection
from letterFinder import letterFinder
from lineExtractor import lineExtractor
from houghBundler import HoughBundler

cap = cv2.VideoCapture(0)

#
# TODO: Find a fix for global variable 'previousLastNumber'
#
paper = paperDetection()
letter = letterFinder()
lineAverage = lineExtractor()
def findparallel(lines):
    lines1 = []
    for i in range(len(lines)):
        for j in range(len(lines)):
            if (i == j):continue
            if (abs(lines[i][1] - lines[j][1]) == 0):
                 #You've found a parallel line!
                 lines1.append((i,j))


    return lines1
previousLastNumber = 0

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

    # lineAverage.update(letter.get(), paper.get())
    #
    # Creating the images of the detected letters
    #

    for index, x in enumerate(letter.get()):
        temporaryFrame = paper.get()[x[3]:x[1], x[0]:x[2]]
        blur = cv2.medianBlur(temporaryFrame, 5)
        cannyFrame = cv2.Canny(blur, 200, 255)

        lines = cv2.HoughLinesP(cannyFrame, 1, np.pi / 180, 11, minLineLength=7, maxLineGap=4)
        mergedLines = []
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                angle = math.atan2(y1 - y2, x1 - x2)
                angle = angle * 180 / math.pi
                mergedLines.append([angle, [x1,y1,x2,y2]])

            mergedLines = sorted(mergedLines, key=lambda x: x[0])
            print('\n')
            # print(mergedLines)
            newMergedArray = []
            previousAngle = 0
            for line in mergedLines:
                x1,y1,x2,y2 = line[1]
                length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if len(newMergedArray) > 0:
                    if (previousAngle - 5) < line[0] < (previousAngle + 5):
                        if (length > previousLength):
                            newMergedArray.pop(len(newMergedArray) - 1)
                            newMergedArray.append(line)
                    else:
                            newMergedArray.append(line)
                else:
                    newMergedArray.append(line)

                previousAngle = line[0]
                previousLength = length
                previousObject = line
                # length = cv2.norm((l[2],l[3])-(l[0],l[2]))
            print('mergedlines: ', mergedLines)
            print('newMergedLines: ', newMergedArray)
            for line in newMergedArray:
                x1,y1,x2,y2 = line[1]
                cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # if len(newMergedArray) > 0:
                #     # print(line)
                #     for a in newMergedArray:
                #         print(a)
                #         if (a[0][0] >= 4):
                #             if (a[0][0] - 4) < line[0] < (a[0][0] + 4):
                #                 print(a[0])
                #                 print(line)
                #         else:
                #             if (a[0][0] - 4) > line[0] > (a[0][0] + 4):
                #                 print(a[0])
                #                 print(line)
                #
                #         # print(line[0])
                #         # print(a[0][0])
                #         break
                # else:
                #     newMergedArray.append([line])

            # print(newMergedArray)



            # foos = a.process_lines(lines,temporaryFrame)
            # # loop over every line in image
            # for foo in foos:
            #     x1 = foo[0][0]
            #     y1 = foo[0][1]
            #     x2 = foo[1][0]
            #     y2 = foo[1][1]
            #     angle = math.atan2(y1 - y2, x1 - x2)
            #     angle = angle * 180 / math.pi
            #     if 85 < angle < 95:
            #         cv2.line(temporaryFrame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            #     elif 175 < angle < 185:
            #         cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #     elif 100 < angle < 170 or -100 > angle > -170:
            #         cv2.line(temporaryFrame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # DEBUG CODE
            cv2.imshow('t' + str(index), temporaryFrame)
        #             cv2.imshow('a' + str(index), blur)
        #             cv2.imshow('c' + str(index), cannyFrame)
        #
    for x in range(len(letterArray), previousLastNumber):
        cv2.destroyWindow('t' + str(x))
    #             cv2.destroyWindow('a'+str(x))
    #             cv2.destroyWindow('c'+str(x))
    previousLastNumber = len(letterArray)


    # for x in lineAverage.get():
    #     if x[0] == 10:
    #         # print(averageArray)
    #         newAverageArray = lineAverage.get()
    #         lineAverage.clean()
    #         print(' ')
    #         for a in newAverageArray:
    #             if a[0] > 5:
    #                 horizontalAvg = a[1]/a[0]
    #                 verticalAvg = a[2]/a[0]
    #                 diagonalAvg = a[3]/a[0]
    #                 print('Horizontal: ', horizontalAvg, 'Vertical: ', verticalAvg, 'Diagonal: ', diagonalAvg)
    #
    #                 for l in letterArray:
    #                     # print(l[0])
    #                     # print(l[1], horizontalAvg, l[2])
    #                     if l[1] <= horizontalAvg <= l[2]:
    #                         # print('worked')
    #                         # print(l[3], verticalAvg, l[4])
    #                         if l[3] <= verticalAvg <= l[4]:
    #                             # print('worked1')
    #                             if l[5] <= diagonalAvg <= l[6]:
    #                                 print('target = ', l[0])
    #                                 break;
    #         break

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
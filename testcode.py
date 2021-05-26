import cv2
import numpy as np
import math
from paperDetection import paperDetection
from letterFinder import letterFinder
from lineExtractor import lineExtractor

cap = cv2.VideoCapture(0)

#
# TODO: Find a fix for global variable 'previousLastNumber'
#
paper = paperDetection()
letter = letterFinder()
lineAverage = lineExtractor()

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

    lineAverage.update(letter.get(), paper.get())
    #
    # Creating the images of the detected letters
    #



    for x in lineAverage.get():
        if x[0] == 10:
            # print(averageArray)
            newAverageArray = lineAverage.get()
            lineAverage.clean()
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
    # NOTE: Disable properly (20ms wait for better performance)
    #
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#
# When everything done, release the capture
#
cap.release()
cv2.destroyAllWindows()
import cv2
from paperDetection import PaperDetection
from letterFinder import LetterFinder
from lineExtractor import LineExtractor

cap = cv2.VideoCapture(0)

#
# TODO: Find a fix for global variable 'previousLastNumber'
#
paper = PaperDetection()
letter = LetterFinder()
lineAverage = LineExtractor()

wordArray = [
    ['Den Haag', 'D', 'E', 'N'],
    ['Alkmaar', 'A', 'L', 'K']

]

while True:
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

    targetArray = []

    for x in lineAverage.get():
        if x[0] == 10:
            averageArray = lineAverage.get()
            lineAverage.clean()
            for averageValue in averageArray:
                if averageValue[0] > 5:
                    horizontalAvg = averageValue[1] / averageValue[0]
                    verticalAvg = averageValue[2] / averageValue[0]
                    diagonalAvg = averageValue[3] / averageValue[0]

                    flag = 0
                    for letter in letterArray:
                        if letter[1] <= horizontalAvg <= letter[2]:
                            if letter[3] <= verticalAvg <= letter[4]:
                                if letter[5] <= diagonalAvg <= letter[6]:
                                    flag = 1
                                    targetArray.append(letter[0])
                                    break
                    if flag == 0:
                        targetArray.append('')
            break

    for word in wordArray:
        if (len(word) - 1) <= len(targetArray):
            strike = 0
            for targetIndex, targetValue in enumerate(targetArray):
                if word[targetIndex] != targetValue:
                    strike = strike + 1
                if strike > 1:
                    print('The word is not:', word[0])
                    break
            if strike < 2:
                print('The word is: ', word[0])
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

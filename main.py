import cv2
from paperDetection import paperDetection
from letterFinder import letterFinder
from lineExtractor import lineExtractor

cap = cv2.VideoCapture(0)

paper = paperDetection()
letter = letterFinder()
lineAverage = lineExtractor()

wordArray = [
    ['Den Haag', 'D','E','N'],
    ['Alkmaar', 'A', 'L', 'K']
]

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


def cameraDetection():
    stopFlag = False
    while(True):
        ret, frame = cap.read()

        paper.update(frame)
        cv2.imshow('test', paper.get())

        letter.update(paper.get())

        lineAverage.update(letter.get(), paper.get())

        targetArray = []

        for x in lineAverage.get():
            if x[0] == 10:
                newAverageArray = lineAverage.get()
                lineAverage.clean()
                for a in newAverageArray:
                    if a[0] > 5:
                        horizontalAvg = a[1]/a[0]
                        verticalAvg = a[2]/a[0]
                        diagonalAvg = a[3]/a[0]

                        flag = 0
                        for l in letterArray:
                            if l[1] <= horizontalAvg <= l[2]:
                                if l[3] <= verticalAvg <= l[4]:
                                    if l[5] <= diagonalAvg <= l[6]:
                                        flag = 1
                                        targetArray.append(l[0])
                                        break
                        if flag == 0:
                            targetArray.append('')
                break

        if len(targetArray) > 0:
            print(targetArray)
            for word in wordArray:
                # print((len(word) - 1), len(targetArray))
                if (len(word) - 1) <= len(targetArray):
                    strike = 0
                    for targetIndex, targetValue in enumerate(targetArray):
                        # print('Word: ', word[targetIndex + 1],'Target: ', targetValue)
                        if word[targetIndex + 1] != targetValue:
                            strike = strike + 1
                        if strike > 1:
                            # print('The word is not:', word[0])
                            break
                    if strike < 2:
                        print('The word is: ', word[0])
                        stopFlag = True
                        break

    #
    # NOTE: Disable properly (20ms wait for better performance)
    #
        if cv2.waitKey(20):
            if 0xFF == ord('q') or stopFlag == True:
                break

        # if cv2.waitKey(20) & 0xFF == ord('q'):
        #     break

#
# When everything done, release the capture
#


if __name__ == '__main__':
    cameraDetection()
    cap.release()
    cv2.destroyAllWindows()
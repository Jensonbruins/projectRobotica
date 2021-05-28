import cv2
from wordDetection.paperDetection import paperDetection
from wordDetection.letterFinder import letterFinder
from wordDetection.lineExtractor import lineExtractor

class image():
    def __init__(self):
        self.paper = paperDetection()
        self.letter = letterFinder()
        self.lineAverage = lineExtractor()

        self.wordArray = [
            ['Den Haag', 'D', 'E', 'N'],
            ['Alkmaar', 'A', 'L', 'K']
        ]

        self.letterArray = [
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
    def cameraDetection(self,cap):
        stopFlag = False
        globalWord = 0
        while(True):
            ret, frame = cap.read()

            self.paper.update(frame)
            cv2.imshow('test', self.paper.get())

            self.letter.update(self.paper.get())

            self.lineAverage.update(self.letter.get(), self.paper.get())

            targetArray = []

            for x in self.lineAverage.get():
                if x[0] == 10:
                    newAverageArray = self.lineAverage.get()
                    self.lineAverage.clean()
                    for a in newAverageArray:
                        if a[0] > 5:
                            horizontalAvg = a[1]/a[0]
                            verticalAvg = a[2]/a[0]
                            diagonalAvg = a[3]/a[0]

                            flag = 0
                            for l in self.letterArray:
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
                for word in self.wordArray:
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
                            # print('The word is: ', word[0])
                            globalWord = word[0]
                            stopFlag = True
                            break

        #
        # NOTE: Disable properly (20ms wait for better performance)
        #
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if stopFlag:
                return globalWord
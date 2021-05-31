import cv2
from wordDetection.paperDetection import paperDetection
from wordDetection.letterFinder import letterFinder
from wordDetection.lineExtractor import lineExtractor
from wordDetection.letterConverter import letterConverter


class image():
    def __init__(self):
        self.paperDetection = paperDetection()
        self.letterFinder = letterFinder()
        self.lineExtractor = lineExtractor()
        self.letterConverter = letterConverter()

        self.wordArray = [
            ['Den Haag', 'D', 'E', 'N'],
            ['Alkmaar', 'A', 'L', 'K']
        ]
    def cameraDetection(self,cap):
        stopFlag = False
        globalWord = 0
        while(True):
            ret, frame = cap.read()

            detectedPaperFrame = self.paperDetection.update(frame)

            contourArray = self.letterFinder.update(detectedPaperFrame)
            # print(contourArray)
            if contourArray is not None:
                averageArray = self.lineExtractor.update(contourArray, detectedPaperFrame)
                print(averageArray)
                targetArray = self.letterConverter.get(averageArray, self.lineExtractor)


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
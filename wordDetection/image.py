import cv2
from wordDetection.paperDetection import paperDetection
from wordDetection.letterFinder import letterFinder
from wordDetection.lineExtractor import lineExtractor
from wordDetection.letterConverter import letterConverter
from wordDetection.wordConverter import wordConverter

class image():
    def __init__(self):
        self.paperDetection = paperDetection()
        self.letterFinder = letterFinder()
        self.lineExtractor = lineExtractor()
        self.letterConverter = letterConverter()
        self.wordConverter = wordConverter()


    def cameraDetection(self,cap):
        stopFlag = False
        globalWord = 0
        while(True):
            ret, frame = cap.read()
            frame = cv2.flip(frame,-1)
            cv2.imshow('test', frame)
            detectedPaperFrame = self.paperDetection.update(frame)

            contourArray = self.letterFinder.update(detectedPaperFrame)
            # print(contourArray)
            if contourArray is not None:
                averageArray = self.lineExtractor.update(contourArray, detectedPaperFrame)

                targetArray = self.letterConverter.get(averageArray, self.lineExtractor)

                stopFlag, globalWord = self.wordConverter.get(targetArray)

        #
        # NOTE: Disable properly (20ms wait for better performance)
        #
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if stopFlag:
                return globalWord
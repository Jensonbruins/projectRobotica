import cv2
import numpy as np

class wordConverter():
    def __init__(self):
        self.wordArray = [
            ['Den Haag', 'D', 'E', 'N'],
            ['Alkmaar', 'A', 'L', 'K']
        ]

    def get(self, targetArray):
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
                        return True, word[0]
        return False, None
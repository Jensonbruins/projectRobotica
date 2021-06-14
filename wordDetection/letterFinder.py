import cv2
from wordDetection.lineExtractor import lineExtractor

class letterFinder():
    def __init__(self):
        self.lineExtractor = lineExtractor()
        self.offset = 50

    def search(self, frame):
        word = False
        array = []
        ret, croppedFrameThreshold = cv2.threshold(frame, 100, 255,
                                                   cv2.THRESH_BINARY_INV)
        edged = cv2.cvtColor(croppedFrameThreshold, cv2.COLOR_BGR2GRAY)

        if frame.size > 55000:
            i = 0
            newContours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for index, cnt in enumerate(newContours):
                x, y, w, h = cv2.boundingRect(cnt)
                dimensions = edged.shape
                offset = self.offset
                if x > offset and x < (dimensions[1] - offset) and y > offset and y < (dimensions[0] - offset):
                    if w > 22 and w < 100 and h > 25 and h < 100:
                        size = cv2.contourArea(cnt)
                        if size < 3000:
                            offset = 2
                            north = x - offset
                            east = (y + h) + offset
                            south = (x + w) + offset
                            west = y - offset
                            if north < 0:
                                north = 0
                            if east < 0:
                                east = 0
                            if south < 0:
                                south = 0
                            if west < 0:
                                west = 0
                            array.insert(i, [north, east, south, west])
                            cv2.rectangle(croppedFrameThreshold, (north, west), (south, east), (0, 215, 255), 2)
                            i = i + 1
            
            sorter = lambda x: (x[0], x[1], x[2], x[3])
            sorted_array = sorted(array, key=sorter)
            if array is not None:
                word = self.lineExtractor.extract(sorted_array, frame)

            cv2.imshow('letterFinder', croppedFrameThreshold)
            return word

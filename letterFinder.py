import cv2


class LetterFinder:
    def __init__(self):
        self.frame = 0
        self.offset = 50
        self.array = []

    def get(self):
        return self.array

    def update(self, frame):
        self.array = []
        ret, croppedFrameThreshold = cv2.threshold(frame, 100, 255,
                                                   cv2.THRESH_BINARY_INV)
        edged = cv2.cvtColor(croppedFrameThreshold, cv2.COLOR_BGR2GRAY)

        if frame.size > 100000:
            i = 0
            contourArray, hierarchyArray = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contourValue in contourArray:
                x, y, w, h = cv2.boundingRect(contourValue)
                dimensions = edged.shape
                offset = self.offset
                if offset < x < (dimensions[1] - offset) and offset < y < (dimensions[0] - offset):
                    if 25 < w < 100 and 25 < h < 100:

                        size = cv2.contourArea(contourValue)
                        if size < 3000:
                            north = x - 5
                            east = (y + h) + 5
                            south = (x + w) + 5
                            west = y - 5
                            if north < 0:
                                north = 0
                            if east < 0:
                                east = 0
                            if south < 0:
                                south = 0
                            if west < 0:
                                west = 0
                            self.array.insert(i, [north, east, south, west])
                            # cv2.rectangle(croppedFrame, (north, west), (south, east), (0, 215, 255), 2)
                            i = i + 1
            self.array = self.array[::-1]
            cv2.imshow('test', croppedFrameThreshold)

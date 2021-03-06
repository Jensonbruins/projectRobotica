from wordDetection.wordConverter import wordConverter

class letterConverter():
    def __init__(self):
        self.wordConverter = wordConverter()
        self.letterArray = [
            #   ['letter', horizontalMin, horizontalMax, verticalMin, verticalMax, diagonalMin, diagonalMax]
            ['A', 0.9, 2, 0, 0.2, 7.5, 9.1],
            ['B', 5.5, 6.5, 4.5, 7, 2, 3],
            ['C', 0, 0, 0, 0, 0, 0],
            ['D', 3, 4.5, 3.5, 5.5, 2.5, 4],
            ['E', 5.5, 7.5, 1.5, 3.5, 0, 0.5],
            # ['F', 0, 0, 0, 0, 0, 0],
            # ['G', 0, 0, 0, 0, 0, 0],
            ['H', 1.5, 2.5, 3.6, 4.6, 0, 0.5],
            # ['I', 0, 0, 0, 0, 0, 0],
            # ['J', 0, 0, 0, 0, 0, 0],
            ['K', 0, 0.8, 1.8, 3, 6.5, 8],
            ['L', 1.8, 3, 0.7, 2.5, 0, 0.5],
            ['M', 0.5, 1.5, 4, 5, 5.5, 6.8],
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

    def convert(self, averageArray):
        targetArray = []
        for a in averageArray:
            if a[0] > 5:
                horizontalAvg = a[1] / a[0]
                verticalAvg = a[2] / a[0]
                diagonalAvg = a[3] / a[0]
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

        return self.wordConverter.convert(targetArray)
        # print(targetArray)

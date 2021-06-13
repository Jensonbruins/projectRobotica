class wordConverter():
    def __init__(self):
        self.wordArray = [
            ['Den Haag', 'D', 'E', 'N'],
            ['Alkmaar', 'A', 'L', 'K'],
            ['Haarlem', 'H','L','M']
        ]

    def convert(self, targetArray):
        if len(targetArray) > 0:
            print(targetArray)
            for word in self.wordArray:
                if (len(word) - 1) <= len(targetArray):
                    strike = 0
                    for targetIndex, targetValue in enumerate(targetArray):
                        if word[targetIndex + 1] != targetValue:
                            strike = strike + 1
                        if strike > 1:
                            break
                    if strike < 2:
                        return word[0]
        return False
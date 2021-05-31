class Pad:
    def __init__(self):
        self.vectoren = []

    def set_vector(self, richting, afstand):
        vector = Vector(richting, afstand)
        self.vectoren.append(vector)

    def get_vector(self):
        vector = self.vectoren.pop(0)
        return vector


class Vector:
    def __init__(self, richting, afstand):
        # de te draaien richting in graden
        self.richting = richting
        # de te rijden afstand in cm
        self.afstand = afstand

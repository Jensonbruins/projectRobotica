import math


class Wiel:
    def __init__(self):
        # de radius van het wiel in cm
        self.radius = None
        # de omtrek van het wiel in cm
        self.omtrek = None
        # aantal stappen voor volledige rotatie
        self.volstap = None
        # stap in graden
        self.stapgrote = None
        # de identificatie het wiel op de robot m.b.v. pic uart identifier
        self.identificatie = ""
        # de afstand van het midden tot het wiel lengte, breedte in cm
        self.afstandWiel = [None, None]

    def set_wiel(self, wielPlaatsing):
        self.radius = 2.99
        self.volstap = 2052
        self.identificatie = wielPlaatsing
        self.afstandWiel = [4.05, 6.05]
        self.omtrek = 2 * self.radius * math.pi
        self.stapgrote = self.omtrek / self.volstap

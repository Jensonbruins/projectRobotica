from PathFolower import rijinstructie, wielinstrucitie
import math


class Instructiemaker:
    def __init__(self):
        self.rijinstructies = rijinstructie.Rijinstructie()

    def maak_instructie(self, wielen, vector):
        if vector.richting != 0:
            wielDraaiinstructieArray = []
            for i in wielen:
                wielDraaiinstructieArray.append(wielinstrucitie.Wielinstructie(i))

            self.bereken_draai(wielDraaiinstructieArray, vector.richting)
            self.rijinstructies.wielinstructies.append(wielDraaiinstructieArray)

        if vector.afstand != 0:
            wielRijinstructieArray = []
            for i in wielen:
                wielRijinstructieArray.append(wielinstrucitie.Wielinstructie(i))

            self.bereken_rijden(wielRijinstructieArray, vector.afstand)
            self.rijinstructies.wielinstructies.append(wielRijinstructieArray)

    def bereken_draai(self, wielen, graden):
        for i in wielen:
            # afstand wiel naar middenpunt in de breedte
            wm = i.wiel.afstandWiel[1]
            # diameter wiel
            dw = i.wiel.radius * 2
            # aantal stappen in een rotatie
            sr = i.wiel.volstap

            # aantal stappen = ((wm * π * (graden / 360)) / dw) * sr
            wielafstand = wm * math.pi * (graden / 360)
            rotaties = wielafstand / dw
            stappen = rotaties * sr

            if stappen > 0:
                if i.wiel.identificatie[0] == "r":
                    directie = "v"
                else:
                    directie = "a"
            else:
                stappen *= -1
                if i.wiel.identificatie[0] == "r":
                    directie = "a"
                else:
                    directie = "v"

            self.schrijf_instructie(i, stappen, directie, graden)

    def bereken_rijden(self, wielen, afstand):
        for i in wielen:
            stappen = afstand / i.wiel.stapgrote

            if stappen > 0:
                directie = "v"
            else:
                stappen *= -1
                directie = "a"

            self.schrijf_instructie(i, stappen, directie)

    # maak met behulp van de te zetten stappen een message voor het geselecteerde wiel maken en zet deze in het wielinstructie
    def schrijf_instructie(self, geselecteerdeWiel, stappen, directie, graden = 0):
        geselecteerdeWiel.draai = graden
        stappen = int(stappen)
        if stappen < 256:
            msg = bytes(geselecteerdeWiel.wiel.identificatie, 'utf-8') + bytes([stappen]) + bytes([1]) + bytes(directie, 'utf-8') + bytes(geselecteerdeWiel.wiel.identificatie, 'utf-8')
        else:
            char2 = 0
            moduloTracker = 100000
            while True:
                char2 += 1
                char1 = int(stappen / char2)
                if char1 < 256 and char2 < 256:
                    if stappen % char2 == 0:
                        break
                    else:
                        if char1 % char2 < moduloTracker:
                            moduloTracker = char1 % char2
                            tempchar1 = char1
                            tempchar2 = char2

                if char2 > 255:
                    char1 = int(tempchar1)
                    char2 = int(tempchar2)
                    break
            msg = bytes(geselecteerdeWiel.wiel.identificatie, 'utf-8') + bytes([char1]) + bytes([char2]) + bytes(directie, 'utf-8') + bytes(geselecteerdeWiel.wiel.identificatie, 'utf-8')

        geselecteerdeWiel.instructie = msg

from wordDetection.image import image
from PathFolower import instructiemaker, wiel, pad, uarthandeler, kompas
import cv2, time, sys, signal, atexit, math

cap = cv2.VideoCapture(0)


def setup_wielen():
    wiel1 = wiel.Wiel()
    wiel1.set_wiel("lv")
    wiel2 = wiel.Wiel()
    wiel2.set_wiel("la")
    wiel3 = wiel.Wiel()
    wiel3.set_wiel("rv")
    wiel4 = wiel.Wiel()
    wiel4.set_wiel("ra")
    wielarray = [wiel1, wiel2, wiel3, wiel4]

    return wielarray


def setup_pad():
    padarray = pad.Pad()
    #padarray.set_vector(0, 10)
    padarray.set_vector(90, 0)
    padarray.set_vector(0, 10)
    #padarray.set_vector(-90, 10)

    return padarray


def extra_draai(startRichting):
    # als er gedraaid moet zijn en de draai is niet volledig draai dan extra
    verwachteRichting = richting.lees_richting() + uart.draaicheck
    if verwachteRichting > 360:
        verwachteRichting -= 360
    while uart.draaicheck != 0:
        huidigeRichting = richting.lees_richting()
        berekendeDraai = verwachteRichting - huidigeRichting
        if berekendeDraai < -5 or berekendeDraai > 5:
            extraDraai.set_vector(int(berekendeDraai), 0)
            instructies.rijinstructies.wielinstructies = []
            instructies.maak_instructie(wielen, extraDraai.get_vector())
            uart.stuur_instructie(instructies)
        else:
            uart.draaicheck = 0


if __name__ == '__main__':
    cameraDetection = image()
    volgen = setup_pad()
    extraDraai = pad.Pad()
    wielen = setup_wielen()
    uart = uarthandeler.Uarthandeler()
    richting = kompas.Kompas()

    instructies = instructiemaker.Instructiemaker()

    for i in range(len(volgen.vectoren)):
        beginRichting = richting.lees_richting()
        instructies.rijinstructies.wielinstructies = []
        instructies.maak_instructie(wielen, volgen.get_vector())
        uart.stuur_instructie(instructies)

        extra_draai(beginRichting)

    retval = cameraDetection.cameraDetection(cap)
    print(retval)
    cap.release()
    cv2.destroyAllWindows()
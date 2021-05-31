from wordDetection.image import image
from PathFolower import instructiemaker, pad, uarthandeler, kompas
import utilities
import cv2

cap = cv2.VideoCapture(0)


def setup_pad():
    padarray = pad.Pad()
    padarray.set_vector(90, 0)
    padarray.set_vector(0, 10)

    return padarray


if __name__ == '__main__':
    cameraDetection = image()
    volgen = setup_pad()
    wielen = utilities.setup_wielen()
    uart = uarthandeler.Uarthandeler()
    richting = kompas.Kompas()

    instructies = instructiemaker.Instructiemaker()

    for i in range(len(volgen.vectoren)):
        beginRichting = richting.lees_richting()
        instructies.rijinstructies.wielinstructies = []
        instructies.maak_instructie(wielen, volgen.get_vector())
        uart.stuur_instructie(instructies)

        # uart.extra_draai(beginRichting, instructies, richting)

    retval = cameraDetection.cameraDetection(cap)
    print(retval)
    cap.release()
    cv2.destroyAllWindows()

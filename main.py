from wordDetection.image import image
from PathFolower import instructiemaker, pad, uarthandeler
import utilities
import cv2

cap = cv2.VideoCapture(0)


def setup_pad():
    padarray = pad.Pad()
    padarray.set_vector(0, 30)
    padarray.set_vector(-90, 35)
    padarray.set_vector(-90, 20)

    return padarray


if __name__ == '__main__':
    cameraDetection = image()
    volgen = setup_pad()
    wielen = utilities.setup_wielen()
    uart = uarthandeler.Uarthandeler()

    instructies = instructiemaker.Instructiemaker()

    for i in range(len(volgen.vectoren)):
        instructies.rijinstructies.wielinstructies = []
        instructies.maak_instructie(wielen, volgen.get_vector())
        uart.stuur_instructie(instructies)

        retval = cameraDetection.cameraDetection(cap)
        print(retval)

    cap.release()
    cv2.destroyAllWindows()

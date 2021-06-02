import cv2
from wordDetection.image import image

cap = cv2.VideoCapture(0)

if __name__ == '__main__':
    cameraDetection = image()
    retval = cameraDetection.cameraDetection(cap)
    print(retval)
    cap.release()
    cv2.destroyAllWindows()

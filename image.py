import cv2
from lineExtractor import lineExtractor
from paperDetection import imageConverter

cap = cv2.VideoCapture(0)

convertedFrame = imageConverter()
extractedFrame = lineExtractor()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    convertedFrame.update(frame)
    # convertedFrame = imageConverter(frame)

    # Display the resulting frame
    cv2.imshow('frame', convertedFrame.get())
    cv2.imshow('Original', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
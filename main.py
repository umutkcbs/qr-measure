import cv2
import math
import imutils
import numpy as np
from pyzbar import pyzbar

# your camera device
cap = cv2.VideoCapture(2)

global stat
stat = False

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:

        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        if cv2.waitKey(1) & 0xFF == ord('s'):
            print('select')
            roi = cv2.selectROI(frame)
            print(roi[0], roi[1], roi[2], roi[3])
            stat = True
            frame = cv2.line(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[3] + roi[1]), (0, 255, 0), 3)
            yatayhesap = (500 * roi[2]) / w
            dikeyhesap = (500 * roi[3]) / h
            uzaklik = math.sqrt((yatayhesap * yatayhesap) + (dikeyhesap * dikeyhesap))
            uzaklik = uzaklik / 100
            if uzaklik < 10:
                uzaklik = str(uzaklik)
                uzaklik = uzaklik[0:3] + " cm"
            uzaklik = str(uzaklik)
            uzaklik = uzaklik[0:4] + " cm"
            print(uzaklik)

        if stat:
            frame = cv2.line(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[3] + roi[1]), (10, 180, 0), 3)
            cv2.putText(frame, str(uzaklik), (roi[0], roi[1] - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (10, 180, 0), 2)

    # Display the resulting frame
    cv2.imshow('Measure',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

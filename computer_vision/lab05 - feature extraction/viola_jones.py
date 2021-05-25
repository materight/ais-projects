import cv2 as cv
import numpy as np

# TODO
face_cascade_front_path = ''

cap = cv.VideoCapture(0)

casc_front = cv.CascadeClassifier()
casc_front.load(face_cascade_front_path)

while cap.isOpened():
    _, frame = cap.read()

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    detected = casc_front.detectMultiScale(frame_gray, 1.1, 2, 0 | cv.CASCADE_SCALE_IMAGE, (30, 30))

    for x, y, h, w in detected:
        cv.rectangle(frame, (x,y), (x+w, x+h), (0,0,255), 3)

    cv.imshow('Result', frame)
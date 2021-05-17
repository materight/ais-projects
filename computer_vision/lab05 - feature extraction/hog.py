import numpy as np
import cv2 as cv

cap = cv.VideoCapture('../material/Video.mp4')

# Init the hog detector
hog = cv.HOGDescriptor(
    (64, 128), # Window size
    (16, 16), # Blocks size
    (8, 8), # Block stride
    (8, 8), # Cells size
    9 # Number of histogram bins (directions)
)
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

while cap.isOpened():
    ret, frame = cap.read()

    # COmpute bounding boxes
    rects, weights = hog.detectMultiScale(frame)

    # Plot results
    for rect in rects:
        # rect = x, y, height, width
        cv.rectangle(frame, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255), 2)
    cv.imshow('HOG', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
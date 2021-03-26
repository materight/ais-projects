import numpy as np
import cv2

cap = cv2.VideoCapture(0)

LEARNING_RATE = 0.02
HISTORY = 200
N_MIX_GAUSS = 2
BG_RATIO = 0.5
NOISE_SIGMA = 1

VAR_THRESH = 16
DETECT_SHADOWS = False

# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(HISTORY, N_MIX_GAUSS, BG_RATIO, NOISE_SIGMA)
fgbg = cv2.createBackgroundSubtractorMOG2(HISTORY, VAR_THRESH, DETECT_SHADOWS) # Also with shadow removal

i = 0
while True:
    _, frame = cap.read()

    # Compute foreground mask
    fgmask = fgbg.apply(frame, LEARNING_RATE)
    bg = fgbg.getBackgroundImage()

    # Show results
    cv2.imshow('video', frame)
    cv2.imshow('background', bg)
    cv2.imshow('motion_mask', fgmask)

    i += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
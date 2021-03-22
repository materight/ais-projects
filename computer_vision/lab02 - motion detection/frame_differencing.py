import numpy as np
import cv2

cap = cv2.VideoCapture(0) # '../material/Video.mp4'

N = 5
frames = []
i = 0
ret = True
while ret:
    ret, frame = cap.read()

    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray_frame)
        if i-N >= 0:
            # Compute differencing
            diff = cv2.absdiff(frames[i], frames[i-N])
            
            # Compute threshold to get a binary mask
            _, diff = cv2.threshold(diff, 32, 255, cv2.THRESH_BINARY)

            # Show results
            cv2.imshow('difference', diff)
        cv2.imshow('video', gray_frame)
        
    i += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
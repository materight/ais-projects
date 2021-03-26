import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ALPHA = 0.02
background = None

i, ret = 0, True
while ret:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if background is None:  
        # Set first frame as background 
        background = gray_frame
    else:
        # Compute adaptive background diff 
        diff = cv2.absdiff(gray_frame, background)

        # Compute threshold to get a binary mask
        _, diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

        # Update background model
        background = np.uint8(ALPHA*gray_frame + (1-ALPHA)*background)

        # Show results
        cv2.imshow('video', gray_frame)
        cv2.imshow('background', background)
        cv2.imshow('motion_mask', diff)

        
    i += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


frame_index = 0
prev_frame, prev_corners = None, None
while cap.isOpened():
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame_copy = frame.copy() # Used only to show results

    # Grayscale conversion
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    if frame_index < 5:
        # Extract features
        new_corners = cv.goodFeaturesToTrack(gray_frame, 
            maxCorners=100,
            qualityLevel=0.01,
            minDistance=10,
            blockSize=3,
            useHarrisDetector=False,
            k=0.04 # Used for Harris detector, useless in this case
        )
    else:
        # Track keypoints
        new_corners, status, err = cv.calcOpticalFlowPyrLK(prev_frame, frame, prev_corners, None,
            winSize  = (15,15),
            maxLevel = 2,
            criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        new_corners = new_corners#[status == 1].reshape(-1,1,2)
    
    # Plot keypoints
    new_corners = np.int0(new_corners)
    for i, corner in enumerate(new_corners):
        x, y = corner.ravel()
        cv.circle(frame_copy, (x, y), 3, (i, i*2, 255-i))

    # Show results
    cv.imshow('Good features to track', frame_copy)

    # Update previous variables
    prev_frame, prev_corners = frame.copy(), new_corners
    frame_index += 1

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
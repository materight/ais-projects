import numpy as np
import cv2 as cv

# Meanshift:
# 1) Convert to HSV and manualy select a ROI bounding box
# 2) Compute the histogram over the ROI
# 3) Compute backprojection: find areas in the image with similar histograms

# Camshift:
# Improvement over meanshift:
# - Supports scaling of object
# - Returns rotated bounding box

ALG = 'camshift' # meanshift or camshift 

cap = cv.VideoCapture(0)

# Take first frame for ROI selection
for i in range(10): # Skip initial frames
    _, frame = cap.read()

# ROI selection
c,r,w,h = cv.selectROI('ROI selection', frame, showCrosshair=False)
track_window = (c,r,w,h)
roi = frame[r:r+h, c:c+w]

# Convert to HSV
hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask =  cv.inRange(hsv_roi, np.array([0, 60, 32]), np.array([180, 255, 255])) # Filter histogram values for each channel
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX) # Normalization

# Stup termination criteria
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1) # Maximum of 10 interations or a max distance of the histogram of 1 w.r.t. the initial hist

while True:
    _, frame = cap.read()
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    if ALG == 'meanshift':
        ret, track_window = cv.meanShift(dst, track_window, term_crit)
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
    else:
        ret, track_window = cv.CamShift(dst, track_window, term_crit)
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv.polylines(frame,[pts],True, 255,2)
    
    cv.imshow('img2', img2)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
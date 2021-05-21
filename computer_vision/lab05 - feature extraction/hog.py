import numpy as np
import cv2 as cv
from skimage import exposure, feature

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

    # Compute bounding boxes
    rects, weights = hog.detectMultiScale(frame)
    
    # Recompute HOG features for visualization
    H, hogImage = feature.hog(frame, orientations=9, pixels_per_cell=(16,16), cells_per_block=(2,2), transform_sqrt=True, block_norm='L1', visualize=True)
    hogImage = exposure.rescale_intensity(hogImage, out_range=(50, 255)).astype(np.uint8) # Rescale intensity to make features more visible
    
    # Plot rectangular bounding boxes
    for rect in rects:
        # rect = x, y, height, width
        cv.rectangle(frame, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255), 2)
    
    cv.imshow('HOG features', hogImage)
    cv.imshow('Detected people', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
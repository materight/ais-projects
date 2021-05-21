from typing import Match
import numpy as np
import cv2 as cv

# Read images in grayscale
img_obj = cv.imread('../material/img/book.png', 0) # "book.png" or "box.png"
img_scene = cv.imread('../material/img/box_in_scene.png', 0)

img_obj2 = img_obj.copy()
img_scene2 = img_scene.copy()

'''
Step 1: apply SIFT
'''
# Detect features on the image: compute keypoints and their descriptors
sift = cv.SIFT_create(400)
kp_obj, dsc_obj = sift.detectAndCompute(img_obj, None) 
kp_scene, dsc_scene = sift.detectAndCompute(img_scene, None) 

# Plot extracted keypoints
img_obj = cv.drawKeypoints(img_obj, kp_obj, dsc_obj, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img_scene = cv.drawKeypoints(img_scene, kp_scene, dsc_scene, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

'''
Step 2: compute matching
'''
# Match descriptors between images
bf = cv.BFMatcher(cv.NORM_L2)
matches = bf.match(dsc_obj, dsc_scene)

# Filter out "bad" matches
matches = list(filter(lambda x : x.distance < 150, matches))

# Plot computed matches
img_matches = cv.drawMatches(img_obj, kp_obj, img_scene, kp_scene, matches, None, flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

'''
Step 2: compute stitching
'''
# Get points of good matches and transform to array of tuples
pts_obj = np.float32([ kp_obj[m.queryIdx].pt for m in matches ]).reshape(-1, 1, 2)
pts_scene = np.float32([ kp_scene[m.trainIdx].pt for m in matches ]).reshape(-1, 1, 2)

# Compute homography
H, masked = cv.findHomography(pts_obj, pts_scene, cv.RANSAC) # RANSAC: uses the matches that are more parrallel as possible w.r.t. each other 
print('Homography matrix:\n', H)

# Warp object image using the computed homography
warped_obj = cv.warpPerspective(img_obj2, H, (img_scene2.shape[1], img_scene2.shape[0]))

# Apply threshold to get black colors
warped_mask = cv.inRange(warped_obj, 0, 0)

# Stitch image using the warped mask
img_stitch = img_scene2.copy()
img_stitch[warped_mask == 0] = warped_obj[warped_mask == 0]

# Plot results
cv.imshow('Object SIFT keypoints', img_obj)
cv.imshow('Scene SIFT keypoints', img_scene)
cv.imshow('Keypoints matches', img_matches)
cv.imshow('Warped object', warped_obj)
cv.imshow('Warped object mask', warped_mask)
cv.imshow('Stitching result', img_stitch)
cv.waitKey(0)
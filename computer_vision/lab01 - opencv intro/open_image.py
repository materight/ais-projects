import cv2

# Open an image
image = cv2.imread('../material/Google.jpg', 1) # 1 for RGB, 0 for grayscale

# Show the image
cv2.imshow('image', image)
cv2.waitKey(0) # Delay, 0 = infinite delay, wait for a key to be pressed indefinitely
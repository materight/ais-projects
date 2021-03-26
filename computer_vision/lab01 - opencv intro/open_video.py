import cv2

# Open video
cap = cv2.VideoCapture('../material/Video.mp4') # Video file
# cap = cv2.VideoCapture(0) # Webcam

i = 0
ret = True
while ret:
    # Capture frame
    ret, frame = cap.read()
    
    if ret:
        # Show frame
        cv2.imshow('video', frame)

        # Save frame in image
        cv2.imwrite(f'results/img{i}.jpg', frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    i += 1

cap.release()

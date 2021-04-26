import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

frame = np.zeros((800,800,3),np.uint8)
last_mes = current_mes = np.array((2,1),np.float32)
last_pre = current_pre = np.array((2,1),np.float32)

def mousemove(event, x,y,s,p):
    global frame, current_mes, mes, last_mes, current_pre, last_pre
    last_pre = current_pre
    last_mes = current_mes
    current_mes = np.array([[np.float32(x)],[np.float32(y)]])

    kalman.correct(current_mes)    # Correction
    current_pre = kalman.predict() # Prediction

    lmx, lmy = last_mes[0].astype(int),last_mes[1].astype(int)
    lpx, lpy = last_pre[0].astype(int),last_pre[1].astype(int)
    
    cmx, cmy = current_mes[0].astype(int),current_mes[1].astype(int)
    cpx, cpy = current_pre[0].astype(int),current_pre[1].astype(int)
    
    cv.line(frame, (lmx[0],lmy[0]),(cmx[0],cmy[0]),(0,200,0))
    cv.line(frame, (lpx[0],lpy[0]),(cpx[0],cpy[0]),(0,0,200))


cv.namedWindow("kalman")
cv.setMouseCallback("kalman", mousemove)

# Init kalman filter
kalman = cv.KalmanFilter(
    6, # Number of parameters of the motion equation: (x,y) position + (vx,vy) velocity + (ax,ay) acceleration
    2, # Measurement size: (x,y) position
)
kalman.measurementMatrix = np.array([
    [1,0,0,0,0,0], # x value
    [0,1,0,0,0,0], # y value
], np.float32)
kalman.transitionMatrix = np.array([
    [1,0,1,0,.5,0], # x_t+1 = x_t + vx_t + 0.5 * ax_t
    [0,1,0,1,0,.5], # y_t+1 = y_t + vy_t + 0.5 * ay_t
    [0,0,1,0,1,0],  # vx_t+1 = vx_t + ax_t
    [0,0,0,1,0,1],  # vy_t+1 = vy_t + ay_t
    [0,0,0,0,1,0],  # ax_t+1 = ax_t
    [0,0,0,0,0,1],  # ay_t+1 = ay_t
], np.float32)
kalman.processNoiseCov = np.array([ # Identity matrix
    [1,0,0,0,0,0],
    [0,1,0,0,0,0],
    [0,0,1,0,0,0],
    [0,0,0,1,0,0],
    [0,0,0,0,1,0],
    [0,0,0,0,0,1],
], np.float32) * 0.03
kalman.measurementNoiseCov = np.array([ # Identity matrix
    [1,0],
    [0,1],
], np.float32)

# Run algorithm
while(True):
    cv.imshow('kalman',frame)
    if cv.waitKey(100) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

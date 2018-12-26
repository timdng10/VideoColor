import numpy as np
import cv2

#Needed to blur list of hues together
probabilityDensity = []
lowCutDistance = 10
highCutDistance = 10
variance = 0.1
probabilityDensity = [1 / np.sqrt(2 * np.pi * variance) * np.exp(-(x**2 / (2 * variance))) for x in range(-lowCutDistance, highCutDistance+1)]

def GetColorTheme(hsvImg):
    #Create list of hue values that have a certain brightness or saturation
    hueList = {}
    for row in hsvImg:
        for col in row:
            h, s, v = col
            if(s > 50):
                hueList[h] = hueList.get(h, 0) + 1

    #Find  distribution of hues
    hueDistribution = [0]*180
    for hue, hueCount in hueList.items():
        x = 0
        for prob in probabilityDensity:
            hueDistribution[(hue-lowCutDistance + x) % 180] = hueDistribution[(hue-lowCutDistance + x) % 180] + hueCount * prob
            x = x + 1

    return hueDistribution.index(max(hueDistribution))


vidW = 640
vidH = 480

cap = cv2.VideoCapture('vid1.mov')
cap2 = cv2.VideoCapture('vid2.mp4')
cap3 = cv2.VideoCapture('vid3.mp4')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (vidW,vidH))

while(cap.isOpened() or cap2.isOpened() or cap3.isOpened()):
    ret, frame = cap.read()

    if(ret == False):
        ret, frame = cap2.read()

    if(ret == False):
        ret, frame = cap3.read()

    frame = cv2.resize(frame, (vidW, vidH))

    #Get color theme of frame
    hsvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    small = cv2.resize(hsvImg, (80, 60))
    colorTheme = GetColorTheme(small)

    #Show color of frame on
    cv2.rectangle(hsvImg,(0,0),(50,50), (colorTheme, 255, 255), -1)

    cv2.imshow('image',cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR))
    out.write(cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap2.release()
cap3.release()
out.release()
cv2.destroyAllWindows()

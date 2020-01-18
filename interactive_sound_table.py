############################################
#  Name: Sudheendra                        #
#  Project_Name: Interactive_Sound_Table   #
#  Date Created: 25-12-19                  #
#  Last modified: 25-12-19                 #
############################################

# Importing the required libraries
import cv2
import numpy as np
import pygame

# Initializing the required variables
temp1 = 1000000
temp2 = 1000000
temp3 = 1000000
b1, b2, b3 = True,True,True
songlen = 500
count1, count2, count3 = 0, 0, 0

cap = cv2.VideoCapture(1)       
# To make the webcam video capture window scale to screen size.
cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# Returns the contours of the colours masked
def selected_range(hsv, a, b):
    lower_green = np.array(a)
    upper_green = np.array(b)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((5, 5))
    grad = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cnts = cv2.findContours(grad.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    return cnts

# Starts playing specific soundtracks in specified channels
def playmusic(a1,x):
    pygame.mixer.init()
    channel_1 = pygame.mixer.Channel(x)
    a = pygame.mixer.Sound(r"C:\Users\SURYA\Desktop\{}".format(a1))  # Enter the file location
    channel_1.play(a)

# Returns  the coordinates of the approximate centroid of the object
def distance(cnts):
    cmax = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cmax)
    if w * h > 1000:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        a = len(cmax)
        sum1 = [[0, 0]]
        for i in range(a):
            sum1 += cmax[i]
        avg = sum1 / a
        b = int(avg[0][0])
        c = int((avg[0][1]))
        cv2.circle(frame, (b, c), 3, (0, 0, 255), 2)
        r = (b - 320) * (b - 320) + (c - 240) * (c - 240)      # Distance from the centre of the screen
        return (r)
    else:
        return (0)

# Determines which song has to be played based on the coordinates given according to the input.
def song(r, x):
    if r==0:
        return "empty.wav"
    if r<15000:
        i=1
    if 15000<r<55000:
        i=2
    if r>55000:
        i=3
    return "{}{}.wav".format(x,i)

# Function to continuosly check for change in region/colour of objects in the area seen by the webcam
def check(r1,temp1):
    if r1 <15000:
        if temp1<15000:
            return False
        else:
            return True                                  # The values represent regions on the screen based on the distance 
    elif 15000<r1<55000:                                 # from the centre squared
        if 15000<temp1<55000:
            return False
        else:
            return True
    elif 55000<r1:
        if 200000>temp1>55000:
            return False
        else:
            return True

# The main function to continuosly detect and update the songs to be played
while True:
    ret, frame = cap.read()
    cv2.circle(frame,(320,240),int(15000**0.5),(0,255,0),2)
    cv2.circle(frame, (320, 240),int(55000 ** 0.5), (0, 255, 0), 2)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cnts1 = selected_range(hsv, [29, 86, 6], [100, 255, 255])      # Green
    cnts2 = selected_range(hsv, [110, 50, 50], [130, 255, 255])    # Blue
    cnts3 = selected_range(hsv, [0, 100, 100], [5, 255, 255])      # Red

    r1 = 0
    r2 = 0
    r3 = 0

    if cnts1 != []:
        r1 = distance(cnts1)
    if cnts2 != []:
        r2 = distance(cnts2)
    if cnts3 != []:
        r3 = distance(cnts3)
    if r1==0:                                           
        playmusic('empty.wav',0)
        temp1=1000000
    if r2==0:
        playmusic('empty.wav',1)           # empty.wav is an empty music file which is to be played when nothing is detected
        temp2=1000000
    if r3==0:
        playmusic('empty.wav',2)
        temp3=1000000
    if check(r1,temp1) or check(r2,temp2) or check(r3,temp3):
        a1 = song(r1, 'd')                          # The names of the music files go as follows:
        a2 = song(r2, 'p')                          # d1,d2,d3  p1,p2,p3    t1,t2,t3
        a3 = song(r3, 't')                          # hence such code.
        if check(r1,temp1):
            b1 = True
            count1=0
        if check(r2,temp2):
            b2 = True
            count2=0
        if check(r3,temp3):
            b3 = True
            count3=0
        if b1:
            playmusic(a1,0)
        b1 = False
        count1 = count1 + 1
        if count1 > songlen:
            b1 = True
            count1 = 0
        if b2:
            playmusic(a2,1)
        b2 = False
        count2 = count2 + 1
        if count2 > songlen:
            b2 = True
            count2 = 0
        if b3:
            playmusic(a3,2)
        b3 = False
        count3 = count3 + 1
        if count3 > songlen:
            b3 = True
            count3 = 0
        temp1=r1
        temp2=r2
        temp3=r3
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:  # press escape to exit
        break

cv2.destroyAllWindows()
cap.release()




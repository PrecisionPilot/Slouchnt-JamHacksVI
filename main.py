import cv2
from math import sqrt
import Pose_detection_module as pdm
import time
import threading
import tkinter

# Initialization code
cap = cv2.VideoCapture(0)
pTime = 0
detector = pdm.poseDetector()

# userInput = ""

# The list that stores the max distance (good posture) and min distance (bad posture)
Dist = [] 

# Initialize procedures
def userInputProcedure(x):
    global userInput
    userInput = input(x)

def getDistance():

    # THREADING STUFF
    # In order to run computer vision detection system and ask user input simultaneously, start a thread
    # userInputThread = threading.Thread(target=userInputProcedure, args="type \"y\" in the console to confirm max distance between nose and upper chest")
    # userInputThread.start()

    # Computer vision detection system
    
    # Read image
    global img

    success, img = cap.read()
    img = detector.findPose(img, True)
    lmList = detector.findPosition(img)

    # Get landmarks

    x1, y1 = lmList[11] # left shoulder
    x2, y2 = lmList[12] # right shoulder

    # Get upper chest by averaging landmark 11 and 12
    upperChest = [(x1 + x2) / 2, (y1 + y2) / 2]
    nose = lmList[0]

    # Distance between the nose and chest
    distance = sqrt(abs(upperChest[0] - nose[0]) ** 2 + abs(upperChest[1] - nose[1]) ** 2)
    
    # Store the distance to our list 
    Dist.append(distance)

    # Show image
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    
    

def slouchAlert():
    
    pass


def distancePerFrame():
    pass



#_________________________________________________________________________#

# Introduction and Data Gathering
print("Hello and welcome to $NAMEOFOURSOFTWARE!")

getDistance()
print("----------------------- this is the max distance", Dist[0])

cv2.putText(img, "go slouch", (50,50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
cv2.imshow("Image", img)
cv2.waitKey(1)

time.sleep(5)

getDistance()
print("----------------------- this is the min distance", Dist[1])

#Average of max and min distance 
Threshold = (Dist[0] + Dist[1])/2




#_________________________________________________________________________#
# This piece of code is just for reference for now
# while True:
#     # Read image
#     success, img = cap.read()
#     img = detector.findPose(img, True)
#     lmList = detector.findPosition(img)
    
#     # Calculating FPS
#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

#     # Show image and wait
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)
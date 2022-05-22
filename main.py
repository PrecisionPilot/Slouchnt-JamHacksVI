import cv2
from math import sqrt
import pose_detection_module as pdm
import time
import threading
import tkinter
from playsound import playsound

# Initial variables
cap = cv2.VideoCapture(0)
pTime = 0
detector = pdm.poseDetector()
# userInput = ""
Dist = []
threshold = 0


#_________________________________________________________________________#
# FUNCTIONS
#_________________________________________________________________________#

def userInputProcedure(x):
    global userInput
    userInput = input(x)


def getDistance():
    # THREADING STUFF
    # In order to run computer vision detection system and ask user input simultaneously, start a thread
    # userInputThread = threading.Thread(target=userInputProcedure, args="type \"y\" in the console to confirm max distance between nose and upper chest")
    # userInputThread.start()

    # Computer vision detection system
    global img

    for i in range(2):
        success, img = cap.read()
        h, w, c = img.shape
        
        #text
        text = ["Now Slouch", "Sit Straight"][i == 0]
        cv2.rectangle(img, (0, 0), (w, h), 0, cv2.FILLED)
        cv2.putText(img, text, (50,50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        
        cv2.imshow("Image", img)
        cv2.waitKey(2000)
        
        success, img = cap.read()
        img = detector.findPose(img, True)    
        lmList = detector.findPosition(img)
        
        cv2.imshow("Image", img)
        cv2.waitKey(2000)
    
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
    

def slouchAlert():
    print("STOP IT")
    cv2.putText(img, "DONT SLOUCH BRO", (50,50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1000)
    distancePerFrame()


def distancePerFrame():
    initTime = 0

    while True:
        success, img = cap.read()
        h, w, c = img.shape
        img = detector.findPose(img, True)    
        lmList = detector.findPosition(img)

        # Set time
        currentTime = time.time()
    
        # Get landmarks
        x1, y1 = lmList[11] # left shoulder
        x2, y2 = lmList[12] # right shoulder

        # Get upper chest by averaging landmark 11 and 12
        upperChest = [(x1 + x2) / 2, (y1 + y2) / 2]
        nose = lmList[0]

        # Distance between the nose and chest
        distance = sqrt(abs(upperChest[0] - nose[0]) ** 2 + abs(upperChest[1] - nose[1]) ** 2)
        
        print(distance, threshold)

        # If slouching
        if distance < threshold:
            cv2.rectangle(img, (0, 0), (w, h), (0, 128, 255), cv2.FILLED)
            if initTime + 2 < currentTime:
                slouchAlert()
        # If good posture
        if distance >= threshold:
            initTime = currentTime
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)

#_________________________________________________________________________#
# Runtime
#_________________________________________________________________________#

# Introduction and Data Gathering
print("Hello and welcome to $NAMEOFOURSOFTWARE!")

# Get distance between nose and shoulder
getDistance()
print("----------------------- this is the max distance", Dist[0])
print("----------------------- this is the min distance", Dist[1])

#Average of max and min distance 
threshold = (Dist[0] + Dist[1])/2
print("----------------------- this is the threshold", threshold)

distancePerFrame()

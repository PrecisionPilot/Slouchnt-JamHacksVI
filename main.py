import cv2
from cv2 import sqrt
import pose_detection_module as pdm
import time
import threading

# Initialization code
cap = cv2.VideoCapture(0)
pTime = 0
detector = pdm.poseDetector()

userInput = ""
maxDistance = 0

# Initialize procedures
def userInputProcedure(x):
    global userInput
    userInput = input(x)

def getMaxDistance():
    # In order to run computer vision detection system and ask user input simultaneously, start a thread
    userInputThread = threading.Thread(target=userInputProcedure, args="type \"y\" in the console to confirm max distance between nose and upper chest")
    userInputThread.start()

    # Computer vision detection system
    while userInput == "":
        # Read image
        success, img = cap.read()
        img = detector.findPose(img, True)
        lmList = detector.findPosition(img)

        # Get landmarks
        x1, y1 = lmList[11]
        x2, y2 = lmList[12]

        # Get upper chest by averaging landmark 11 and 12
        upperChest = [(x1 + x2) / 2, (y1 + y2) / 2]
        nose = lmList[0]
        # Pythagorean Theorem
        distance = sqrt(abs(upperChest[0] - upperChest[1]) ** 2 + abs(nose[0] - nose[1]) ** 2)

        # Display distance on screen
        cv2.putText(img, distance, (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # Show image
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
    # Store the distance to maxDistance
    global maxDistance
    maxDistance = distance


# Introduction
print("Hello and welcome to $NAMEOFOURSOFTWARE!")
getMaxDistance()

# This piece of code is just for reference for now
while True:
    # Read image
    success, img = cap.read()
    img = detector.findPose(img, True)
    lmList = detector.findPosition(img)
    
    # Calculating FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Show image and wait
    cv2.imshow("Image", img)
    cv2.waitKey(1)
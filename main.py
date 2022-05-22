# IMPORTS
from hashlib import new
import cv2
from math import sqrt
import Pose_detection_module as pdm
import time
import threading
from tkinter import *
from tkinter import Tk
from tkinter import messagebox
import playsound as playsound
import random

# Initial variables
playMusic = True
slouchSeconds = 3
cap = cv2.VideoCapture(0)
quota = 0
pTime = 0
detector = pdm.poseDetector()
Dist = []
threshold = 0
tips = []
tipText = ""

#Create an instance of Tkinter frame
win = Tk()
win.withdraw()
win.title('Python Guides')
#Set the geometry of Tkinter frame
win.geometry("150x100")
win.config(bg='#FFFFFF')

# Store the tips in "tips" from "tips.txt"
with open("Assets/tips.txt", "r") as f:
    tips = f.read().split("\n")

#_________________________________________________________________________#
# FUNCTIONS
#_________________________________________________________________________#

def rickRoll():
    playsound.playsound("Assets/Never Gonna Give You Up.mp3")

def introScreen():
    success, img = cap.read()
    h, w, c = img.shape

    tipText = random.choice(tips)
    
    texts = ["Tip of the day:", tipText ]
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range (2):
        textsize = cv2.getTextSize(texts[i], font, 1, 2)[0]
    textX = (w - textsize[0]) / 2
    textY = (h + textsize[1]) / 2

    #text tips
    cv2.rectangle(img, (0, 0), (w, h), (98, 73, 119) , cv2.FILLED)
    cv2.putText(img, texts[0], (int(textX), int(textY)), font, 1, (255, 255, 255), 1)
    cv2.putText(img, texts[1], (int(textX), int(textY) + 50), font, 1, (255, 255, 255), 1)
    cv2.imshow("Image", img)
    cv2.waitKey(5000)


def getDistance():
    global img

    # Computer vision detection system
    for i in range(2):
        success, img = cap.read()
        h, w, c = img.shape
        
        #text
        text = ["Now Slouch", "Sit Straight"][i == 0]
        cv2.rectangle(img, (0, 0), (w, h ), (98, 73, 119), cv2.FILLED)
        cv2.putText(img, text, (50, int(h/2) + 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2)
        
        cv2.imshow("Image", img)
        cv2.waitKey(2500)
        
        success, img = cap.read()
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img)
        
        cv2.imshow("Image", img)
        cv2.waitKey(2500)
    
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

        # Ending screen to tell user when to go back to normal
        if i==1:
            cv2.rectangle(img, (0, 0), (w, h), (98, 73, 119), cv2.FILLED)
            cv2.putText(img, "Calibration", (50, int(h/2) - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2)
            cv2.putText(img, "Complete", (70, int(h/2) + 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(2500)

def slouchAlert():
    if playMusic:
        threading.Thread(target=rickRoll).start()
    popUpWindow()

def popUpWindow():
    win.lift()
    win.attributes('-topmost', True)
    win.after_idle(win.attributes,'-topmost', False)
    messagebox.showwarning("Bad Posture Alert", "FIX YOUR POSTURE!")
    Button(win, text='Click Me').pack(pady=50)

def distancePerFrame():
    initTime = 0

    while True:
        success, img = cap.read()
        h, w, c = img.shape
        img = detector.findPose(img, False)
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
        
        # If bad posture
        if distance < threshold:
            cv2.rectangle(img, (0, 0), (w, h), (98, 73, 119), cv2.FILLED)
            if initTime + slouchSeconds < currentTime:
                slouchAlert()
                initTime = currentTime
        
        # If good posture
        if distance >= threshold:
            initTime = currentTime
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)

#_________________________________________________________________________#
# Runtime
#_________________________________________________________________________#

# start the program with the intro screen
introScreen()

# Get distance between nose and shoulder
getDistance()

# Average of max and min distance
threshold = (Dist[0] + Dist[1])/2.2

# Begin the program
distancePerFrame()
import cv2
import pose_detection_module as pdm
import time

cap = cv2.VideoCapture(0)
pTime = 0
detector = pdm.poseDetector()

while True:
    # Read image
    success, img = cap.read()
    img = detector.findPose(img, True)
    lmList = detector.findPosition(img)
    if lmList:
        print(lmList[14])

    # Calculating FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Show image and wait
    cv2.imshow("Image", img)
    cv2.waitKey(1)
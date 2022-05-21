import cv2
import mediapipe as mp
import time

class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, enable_segmentation=False, smooth_segmentation=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Defining variables
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.enable_segmentation, self.smooth_segmentation, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True, hideImage=False, blur=(0, 0)):
        # Convert to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if hideImage:
            h, w, c = img.shape
            cv2.rectangle(img, (0, 0), (w, h), 0, cv2.FILLED)
        elif not blur == (0, 0):  # blur only if not set to imageless
            img = cv2.blur(img, blur)
        if draw:
            # If results are available
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        # If results are available
        if self.results.pose_landmarks:
            # for each landmark..
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
            return lmList



def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()

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

if __name__ == "__main__":
    main()

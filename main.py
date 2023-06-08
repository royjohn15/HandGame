import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon = 0.8, maxHands = 1)

while True:
    success, img = cap.read() # get image frame
    hands, img = detector.findHands(img) # detect hand

    if hands:
        hand = hands[0]
        hand_type = hand["type"]
        fingers = detector.fingersUp(hand)

        print(fingers)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
last_time = time.time()  # Variable to keep track of the last time the random number was generated

while True:
    success, img = cap.read()  # get image frame
    hands, img = detector.findHands(img)  # detect hand

    if hands:
        hand = hands[0]
        hand_type = hand["type"]
        fingers = detector.fingersUp(hand)
        
        current_time = time.time()  # Get the current time
        
        if current_time - last_time >= 3:  # Check if 3 seconds have passed since the last random number generation
            random_number = random.randint(1, 6)  # Generate a random number from 1 to 6
            print("Fingers:", fingers, "Random Number:", random_number)
            last_time = current_time  # Update the last time variable
            
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)



def generate_frames():
		score = 0
		last_time = time.time()  # Variable to keep track of the last time the random number was generated
		while True:
			success, frame = cap.read()  # get image frame
			if not success:
			    break
			else:
			    hands, frame = detector.findHands(frame)  # detect hand

			    if hands:
			        hand = hands[0]
			        hand_type = hand["type"]
			        fingers = detector.fingersUp(hand)

			        current_time = time.time()  # Get the current time

			        if current_time - last_time >= 3:  # Check if 3 seconds have passed since the last random number generation
			            random_number = random.randint(1, 6)  # Generate a random number from 1 to 6
			            print("Fingers:", fingers, "Random Number:", random_number, "Score:", score)
			            if random_number == sum(fingers):
			                print("game over")
			            else:
			                score += sum(fingers)
			            last_time = current_time  # Update the last time variable

			    ret, buffer = cv2.imencode('.jpg', frame)
			    frame = buffer.tobytes()

			    yield (b'--frame\r\n'
			           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
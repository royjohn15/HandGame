import pygame
from pygame.locals import *
import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import threading

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon = 0.8, maxHands = 1)


width, height = (500, 800)
road_w = int(width/1.6)
roadmark_w = int(width/80)
right_lane = width/2 + road_w/4
left_lane = width/2 - road_w/4
speed = 1

min_x = int(width/2 - road_w/2) + 64  # Minimum x-coordinate allowed
max_x = int(width/2 + road_w/2) - 250 # Maximum x-coordinate allowed


pygame.init()
running = True
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Hand Car Game")
screen.fill((60,220,0))
pygame.display.update()

car = pygame.image.load("car.png")
car_loc = car.get_rect()
car_loc.center = right_lane, height*0.8

enemy = pygame.image.load("enemy.png")
enemy_loc = enemy.get_rect()
enemy_loc.center = left_lane, height*0.2

counter = 0
while running:
	counter += 1
	if counter == 10:
		speed += 0.15
		counter = 0

	enemy_loc[1] += speed

	if enemy_loc[1] > height:
		if random.randint(0,1) == 0:
			enemy_loc.center = right_lane, -200
		else:
			enemy_loc.center = left_lane, -200

	if car_loc[0] == enemy_loc[0] and enemy_loc[1] >= car_loc[1] - 128:
		print("Game Over")
		break

	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		if event.type == KEYDOWN:
			if event.key in [K_a, K_LEFT]:
				car_loc = car_loc.move([-int(road_w/2), 0])
			if event.key in [K_d, K_RIGHT]:
				car_loc = car_loc.move([int(road_w/2), 0])

	pygame.draw.rect(
		screen,
		(50,50,50),
		(width/2 - road_w/2, 0, road_w, height)
		)

	pygame.draw.rect(
		screen,
		(255,240,60),
		(width/2 - roadmark_w/2, 0, roadmark_w, height)
		)

	pygame.draw.rect(
		screen,
		(255,255,255),
		(width/2-road_w/2 + roadmark_w * 2, 0, roadmark_w, height)
		)

	pygame.draw.rect(
		screen,
		(255,255,255),
		(width/2+road_w/2 - roadmark_w * 3, 0, roadmark_w, height)
		)
	screen.blit(car, car_loc)
	screen.blit(enemy, enemy_loc)
	pygame.display.update()

	success, frame = cap.read()
	hands, frame = detector.findHands(frame)
	if hands:
		hand = hands[0]
		fingers = detector.fingersUp(hand)

		if sum(fingers) == 5:
			if car_loc[0] > min_x:
				car_loc = car_loc.move([-int(road_w/2), 0])
		if sum(fingers) == 0:
			if car_loc[0] < max_x:
				car_loc = car_loc.move([int(road_w/2), 0])
	cv2.imshow("Image",frame)
pygame.quit()

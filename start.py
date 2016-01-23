import time
import colors
import buttonScan
import random
import thread
import picamera
import subprocess
import uuid

camera = picamera.PiCamera()
randomColors = [[True, False, False], [False, True, False], [False, False, True], [True, True, False], [True, False, True], [False, True, True]]
password = [[True, False, True], [False, True, True], [False, True, True], [False, False, True], [True, False, False], [False, True, False]]
yCoords = [7, 11, 13, 15]
xCoords = [40, 38, 36, 32]

def run():
	matrix = randomizeMatrix()
	lastScan = 0	
	combination = []
	runner = 0	
	while 1:
		colors.handleColors(matrix, 0.0005)
		x = buttonScan.scan()
		if (lastScan is None and x is not None):
			lastScan = x
			combination.append(getColorValue(matrix, x))
			if len(combination) is 6:
				matrix = checkPassword(combination)
				combination = []
				runner = 0
		elif (lastScan is not None and x is None):
			lastScan = x
		runner += 1
		if runner == 500:
			matrix = randomizeMatrix()
			runner = 0

def randomizeMatrix():
	final = [[], [], [], []]
	for x in range(0, len(final)):
		for y in range(0, 4):
			final[x].append(random.choice(randomColors))
	return final

def getColorValue(matrix, buttonPressed):
	x = xCoords.index(buttonPressed[1])
	y = yCoords.index(buttonPressed[0])
	return matrix[x][y]

def checkPassword(combo):
	if combo == password:
		matrix = singleColor([False, True, False])
	else:
		matrix = singleColor([True, False, False])
		name = "image" + str(uuid.uuid4()) + ".jpg"
		camera.capture(name)
		subprocess.call(["./notify.sh"], shell=True)
	return matrix

def singleColor(color):
	final = [[], [], [], []]
	for x in range(0, len(final)):
		for y in range(0, 4):
			final[x].append(color)
	return final


run()

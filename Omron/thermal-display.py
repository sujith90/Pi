#!/etc/bin/python2.7

import pygame, time, sys
from omrond6t import *
from pygame.locals import *
import RPi.GPIO as GPIO

omron = OmronD6T(arraySize=16)


#GPIO Initializers
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
p.ChangeDutyCycle(70.0/10.0)

SCREEN_DIMS = [500, 500]
xSize = 4 
ySize = 4 
arraySize = xSize * ySize
screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption('Omron D6T Temperature Array')
pygame.mouse.set_visible(False)
pygame.init()
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 72)

X = []
Y = []
temp_hit = 0
square = []
center = []
rect = [Rect] * arraySize

cellWidth = (SCREEN_DIMS[0]) / xSize
cellHeight = SCREEN_DIMS[1] / ySize
cellWidthCenter = cellWidth / 2 
if cellHeight > cellWidth:
  cellHeight = cellWidth
cellHeightCenter = cellHeight / 2 

#Calculate cell edge pixel in x direction 
for x in range(xSize):
    X.append(x * cellWidth)

#Calculate cell edge pixel in the y direction
for y in range(ySize):
    Y.append(y*cellWidth) #(y * cellHeight) + (SCREEN_DIMS[1] - cellHeight))

for y in range(ySize):
  for x in range(xSize):
    square.append((X[x], Y[y], cellWidth, cellHeight))
    center.append((X[x] + cellWidthCenter, Y[y] + cellHeightCenter))

def temp_to_rgb(temp):
  if temp < 76:
    return (0, 0, 192)
  elif temp >= 76 and temp < 90:
    return (255, 128, 0)
  elif temp > 90:
    return (255, 0, 0)

hit_start_time = time.time()
hit_time = 11
person_detect = False

text = font.render('Omron D6T Thermal Sensor', 1, (255,255,255))
text_pos = text.get_rect()
text_pos.center = ((SCREEN_DIMS[0])/4,SCREEN_DIMS[1] - cellHeight - 18)
screen.blit(text, text_pos)


# define the function blocks
def center_block():
    p.ChangeDutyCycle(7)
    print "Center Block: Turn on LED & No movement"

def top_center():
    #GPIO.output(17, GPIO.LOW)
    print "Top Center: Turn off LED & Move Camera UP"
    
def bottom_center():
    #GPIO.output(17, GPIO.LOW)
    print "Bottom Center: Turn off LED & Move Camera DOWN"

def right_center():
    p.ChangeDutyCycle(10.5)
    print "Right Center: Turn off LED & Move Camera RIGHT"
    
def left_center():
    p.ChangeDutyCycle(4.5)
    print "Left Center: Turn off LED & Move Camera LEFT"

def top_left():
    p.ChangeDutyCycle(4.5)
    print "Top Left: Turn off LED & Move Camera UP_LEFT"

def top_right():
    p.ChangeDutyCycle(10.5)
    print "Top Right: Turn off LED & Move Camera UP_RIGHT"

def bottom_left():
    p.ChangeDutyCycle(4.5)
    print "Bottom Left: Turn off LED & Move Camera BOTTOM_LEFT"
    
def bottom_right():
    p.ChangeDutyCycle(10.5)
    print "Bottom Right: Turn off LED & Move Camera BOTTOM_RIGHT"

# map the inputs to the function blocks
function = {
            0 : top_left,
            1 : top_center,
            2 : top_center,
            3 : top_right,
            4 : left_center,
            5 : center_block,
            6 : center_block,
            7 : right_center,
            8 : left_center,
            9 : center_block,
            10 : center_block,
            11 : right_center,
            12 : bottom_left,
            13 : bottom_center,
            14 : bottom_center,
            15 : bottom_right
}

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.display.quit()
      sys.exit(0)
    if event.type == KEYDOWN:
      if event.key == K_q or event.key == K_ESCAPE:
        pygame.display.quit()
        sys.exit(0)

  bytes_read, temperature = omron.read()

  temp_hit = 0
  for i in range(arraySize):
    if temperature[i] >= 76:
      temp_hit += 1
    
    print(temperature[i],  i) 
    screen.fill(temp_to_rgb(temperature[i]), square[i])
    if max(temperature) > 76:
	    cell = temperature.index(max(temperature))
	    function[cell]()
    else:
	p.ChangeDutyCycle(7.0)
 
    
    
    #text = font.render(str(i+1), 12, (255,255,255))
    #text_pos = text.get_rect()
    #text_pos.center = (center[i][0], SCREEN_DIMS[1] - cellHeight + 18)
    #screen.blit(text, text_pos)
    text = font.render(str(int(temperature[i]))+" "+str(i+1) + chr(0xb0) + "F", 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = center[i]
    screen.blit(text, text_pos)
  
  #Trigger Person Detection###############################################################
  hit_time = time.time() - hit_start_time

  if temp_hit > 3:
    person_detect = True
    hit_start_time = time.time()
  elif temp_hit <= 3 and hit_time > 10:
    person_detect = False

  if person_detect:    
    #screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],180))
    screen.fill((255,0,0), (0,0,SCREEN_DIMS[0],180))
    text = font2.render('RESERVED', 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,90)
    screen.blit(text, text_pos)
    

  else:
    #screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],180))
    #screen.fill((0,192,0), (0,0,SCREEN_DIMS[0],180))
    text = font2.render('AVAILABLE', 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,90)
    screen.blit(text, text_pos)
    

  pygame.display.update()
  time.sleep(0.01)

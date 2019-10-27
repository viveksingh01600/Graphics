import random, pygame, sys
from pygame.locals import *

#assign speed to the snake
FPS = 15

#assign width to each cell and total window
WINWIDTH = 640
WINHEIGHT = 480
CELLSIZE = 20

assert WINWIDTH % CELLSIZE == 0
assert WINHEIGHT % CELLSIZE == 0

#assign width to each cell
CELLWIDTH = int(WINWIDTH / CELLSIZE)
CELLHEIGHT = int(WINHEIGHT / CELLSIZE)

#setting colors for further use
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY = ( 40,  40,  40)

#set background color
BGCOLOR = BLACK

#set key directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0


def main():
	#main loop for setting up stuff
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	pygame.init()
	
	#set basic speed, display and font
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

	#set caption
	pygame.display.set_caption('Snake')
	showhomeScreen()
	
	#loop for game
	while True:
		runGame()
		gameOverScreen()


def runGame():
	# Set a random start point.
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	
	#set cordinates for snake
	snakeCoords = [{'x': startx,     'y': starty},
				  {'x': startx - 1, 'y': starty},
				  {'x': startx - 2, 'y': starty}]
	
	#ser initial direction for snake
	direction = RIGHT
	
	# Start the fruit in a random place.
	fruit = getRandomLocation()
	
	while True:
		# main game loop
		for event in pygame.event.get():
			# event handling loop
			if event.type == QUIT:
				endgameTer()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					endgameTer()
		
		# check if the snake has hit itself or the edge
		if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
			# game over
			return
		for snakeBody in snakeCoords[1:]:
			if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
				# game over
				return
		
		# check if snake has eaten a fruit
		if snakeCoords[HEAD]['x'] == fruit['x'] and snakeCoords[HEAD]['y'] == fruit['y']:
			# don't remove snake's tail segment
			# set a new fruit somewhere
			fruit = getRandomLocation()
		else:
			# remove snake's tail segment
			del snakeCoords[-1]
		
		# move the snake by adding a segment in the direction it is moving
		if direction == UP:
			newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
		
		#insert a new tail
		snakeCoords.insert(0, newHead)
		#change background for new cell
		DISPLAYSURF.fill(BGCOLOR)
		
		#make changes for new added cell
		drawGrid()
		drawsnake(snakeCoords)
		
		#make a new fruit
		drawfruit(fruit)

		#update score
		writeScore(len(snakeCoords) - 3)
		
		#display updated score
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
	#dispay message on home screen
	pressKeySurf = BASICFONT.render('Press a key to start playing.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINWIDTH - 200, WINHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def collision_with_boundaries(snake_head):
	if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0 :
		#gamaend
		return 1
	else:
		#game end
		return 0
 
def collision_with_self(snake_position):
	snake_head = snake_position[0]
	if snake_head in snake_position[1:]:
		#game end
		return 1
	else:
		#game end
		return 0


def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		endgameTer()
	
	keyUpEvents = pygame.event.get(KEYUP)
	
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		endgameTer()
	
	return keyUpEvents[0].key


def display_final_score(display_text, final_score):
	largeText = pygame.font.Font('freesansbold.ttf',35)
	TextSurf = largeText.render(display_text, True, BLACK)
	TextRect = TextSurf.get_rect()
	TextRect.center = ((display_width/2),(display_height/2))
	display.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(2)


def collision_with_apple(apple_position, score):
	fruit_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
	score += 1
	return apple_position, score
	
	#collission
	if snake_head == apple_position:
		apple_position, score = collision_with_apple(apple_position, score)
		snake_position.insert(0,list(snake_head))


def showhomeScreen():
	#show home screen
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	
	#set text
	titleSurf1 = titleFont.render('Snake!', True, WHITE, DARKGREEN)
	titleSurf2 = titleFont.render('Snake!', True, GREEN)
	
	#set initial rotation for text
	degrees1 = 0
	degrees2 = 0
	
	while True:
		#text 1
		DISPLAYSURF.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINWIDTH / 2, WINHEIGHT / 2)
		
		#text 2
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINWIDTH / 2, WINHEIGHT / 2)
		
		#rotate text
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
		drawPressKeyMsg()
		
		if checkForKeyPress():
			# clear event queue
			pygame.event.get()
			# endgame
			return
		
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
		# rotate by 3 degrees each frame
		degrees1 += 3
		# rotate by 7 degrees each frame
		degrees2 += 7


def endgameTer():
	#quit when exit
	pygame.quit()
	sys.exit()


def display_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display,red,pygame.Rect(position[0],position[1],10,10))
 
def display_apple(display,apple_position, apple):
    display.blit(apple,(apple_position[0], apple_position[1]))


def getRandomLocation():
	return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def gameOverScreen():
	#display final game over screen and text
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	
	#set position of text
	gameRect.midtop = (WINWIDTH / 2, 10)
	overRect.midtop = (WINWIDTH / 2, gameRect.height + 10 + 25)
	
	#disply over the main screen
	DISPLAYSURF.blit(gameSurf, gameRect)
	DISPLAYSURF.blit(overSurf, overRect)
	
	#check for key press
	drawPressKeyMsg()

	#update and display changes
	pygame.display.update()
	pygame.time.wait(500)
	
	# clear out any key presses in the event queue
	checkForKeyPress()
	
	while True:
		if checkForKeyPress():
			# clear event queue
			pygame.event.get()
			#endgame
			return


def writeScore(score):
	#write score on screen
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()

	#set position
	scoreRect.topleft = (WINWIDTH - 120, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawsnake(snakeCoords):
	for coord in snakeCoords:
		#set cordinated for new cell
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		
		#add new segment
		snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
		
		#change inner color of snake
		snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(DISPLAYSURF, GREEN, snakeInnerSegmentRect)


def drawfruit(coord):
	#get cordinated of fruit
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE

	#Add new color to fruit
	fruitRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(DISPLAYSURF, RED, fruitRect)


def drawGrid():
	for x in range(0, WINWIDTH, CELLSIZE):
		# draw vertical lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINHEIGHT))
	for y in range(0, WINHEIGHT, CELLSIZE):
		# draw horizontal lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINWIDTH, y))


if __name__ == '__main__':
	main()

# Script: dwarfgame.py
# Author: Andrew Smith
# Description: A python script to test / experiment with video game AI and Mathematics

import pygame
import os
import threading
import time
from pygame.locals import *
from time import sleep

# Initialise the PyGame module
pygame.mixer.pre_init(44100, -16,2,2048)
pygame.init()

#######################################
##########	 SCREEN SETTINGS	#######
#######################################

# Define Horiz Resolution
HORIZ_RESOLUTION = 1600
# Define Vertical Resolution 
VERT_RESOLUTION = 1200
# Define Screen Fill Colour
SCREEN_FILL_COLOUR = [0, 0, 0] # Black

#######################################################
##													###
##			DIRECTION INDICATOR VALUES				###
##													###
#######################################################

UP_DIRECTION = 1
RIGHT_DIRECTION = 3
DOWN_DIRECTION = 5
LEFT_DIRECTION = 7

#######################################
#####	 CLASS CREATION	   ############
#######################################

#######	  PLAYER Class	 ##########

class Player:
	# Class Constructor
	def __init__(self, playerNameIn):
		# Set Player Name
		self.name = playerNameIn
		
		# Set player position to middle of screen (by default)
		self.x = (HORIZ_RESOLUTION/2)
		self.y = (VERT_RESOLUTION/2)
		
		# Set the direction the player is facing
		self.direction_indicator = UP_DIRECTION
		
		# Set player starting location
		self.location = 'PLAYROOM'
		
		# Set player energy
		self.energy = 100
		
		# Set player gold
		self.gold = 0
		
		# Set player angle
		self.walk_angle = 10
		
		# Set player target angle
		self.walk_target_angle = 0
		
		# Identify attack sequence
		self.attack = False		
		
	def processWalk_Anim(self, directionHeadingIn):	
		# Process UP direction animation sequence
		
		if directionHeadingIn == UP_DIRECTION:
			if self.direction_indicator != UP_DIRECTION:
				self.direction_indicator = UP_DIRECTION
				self.walk_angle = 0
				self.walk_target_angle = 0				
			
			# Manage the animation walk (the stagger walk)

			if self.walk_angle > self.walk_target_angle:
				self.walk_angle = self.walk_angle - 1				
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == 0:				
				self.walk_target_angle = 10				
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == 10:
				self.walk_target_angle = 0				
			
			if self.walk_angle < self.walk_target_angle:
				self.walk_angle = self.walk_angle + 1
			
		# Process Right direction animation sequence
		if directionHeadingIn == RIGHT_DIRECTION:
			if self.direction_indicator != RIGHT_DIRECTION:
				self.direction_indicator = RIGHT_DIRECTION
				self.walk_angle = -90
				self.walk_target_angle = -80
		
			# Manage the walk animation
			if self.walk_angle < self.walk_target_angle:
				self.walk_angle = self.walk_angle + 1
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == -90:
				self.walk_target_angle = -80
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == -80:
				self.walk_target_angle = -90
			
			if self.walk_angle > self.walk_target_angle:
				self.walk_angle = self.walk_angle - 1
			
		# Process DOWN direction animation sequence
		if directionHeadingIn == DOWN_DIRECTION:
			if self.direction_indicator != DOWN_DIRECTION:
				self.direction_indicator = DOWN_DIRECTION
				self.walk_angle = 180				
				self.walk_target_angle = 170			
		
			# Manage the animation walk
			if self.walk_angle > self.walk_target_angle:
				self.walk_angle = self.walk_angle - 1
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == 170:
				self.walk_target_angle = 180
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == 180:
				self.walk_target_angle = 170
			
			if self.walk_angle < self.walk_target_angle:
				self.walk_angle = self.walk_angle + 1  
			
		# Process LEFT direction animation sequence
		if directionHeadingIn == LEFT_DIRECTION:
			if self.direction_indicator != LEFT_DIRECTION:
				self.direction_indicator = LEFT_DIRECTION
				self.walk_angle = -270
				self.walk_target_angle = -260
		
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == -260:
				self.walk_target_angle = -270
			
			if self.walk_angle == self.walk_target_angle and self.walk_target_angle == -270:
				self.walk_target_angle = -260
			
			if self.walk_angle < self.walk_target_angle:
				self.walk_angle = self.walk_angle + 1
			
			if self.walk_angle > self.walk_target_angle:
				self.walk_angle = self.walk_angle - 1
	
	# Attack move
	def performAttack_Move(self, directionHeadingIn):
		if directionHeadingIn == UP_DIRECTION:
			self.walk_angle = self.walk_angle - 5
			
			if self.walk_angle < 5:
				#sleep(0.1)
				self.attack = False
				
		if directionHeadingIn == RIGHT_DIRECTION:
			self.walk_angle = self.walk_angle - 5
			
			if self.walk_angle < -90:
				#sleep(0.1)
				self.attack = False
				
		if directionHeadingIn == DOWN_DIRECTION:
			self.walk_angle = self.walk_angle - 5
			
			if self.walk_angle < -180:
				#sleep(0.1)
				self.attack = False
				self.walk_angle = 180				
				self.walk_target_angle = 170
				
		if directionHeadingIn == LEFT_DIRECTION:
			self.walk_angle = self.walk_angle - 5
			
			if self.walk_angle < -270:
				#sleep(0.1)
				self.attack = False
	
	

##########	  DWARF PLAYER CLASS   #########

class DwarfPlayer(Player):
	def __init__(self, PlayerNameIn):
		super().__init__(PlayerNameIn)
		self.hasAxe = False
		self.hasShield = False
		
	# Display Player status
	def displayStatus(self, screenIn):
		self.testtext = create_text(str(self.location), 22, (0, 128, 0))
		self.player_life = create_text(str(self.energy), 22, (0, 128, 0))
		self.gold_amount = create_text(str(self.gold), 22, (0, 128, 0))

		# Output Player statistics 
		screenIn.blit(player_stats, (round((self.x+300)), round((self.y-550))))
		screenIn.blit(heart_icon, (round((self.x+310)), round((self.y-500))))
		screenIn.blit(gold_icon, (round((self.x+420)), round((self.y-500))))
		screenIn.blit(self.gold_amount, (round((self.x+460)), round((self.y-500))))
		screenIn.blit(self.player_life, (round((self.x+360)), round((self.y-500))))	
		screenIn.blit(self.testtext, (round((self.x+310)), round((self.y-550))))	

##########	  AI DWARF CLASS	############

class DwarfAIPlayer(Player):
	def __init__(self, PlayerNameIn):
		super().__init__(PlayerNameIn)
		self.hasAxe = False
		self.hasShield = False
		self.name = PlayerNameIn
		
		# Set position
		self.x = 100
		self.y = 100
		
		# Set attack possible flag
		self.attackPossible = False
		
		# Identify when in range of human player
		self.inRange = False
		
		# Identify when to stop moving
		self.stopMoving = False
		
		self.angle_build = 0
		self.noOfAttacks = 0
		self.firstAttackPart = False
		self.secondAttackPart = False
		self.attackComplete = False
		
	def attackMove(self):
		# Attack swing out
		if self.firstAttackPart == False and self.secondAttackPart == False:
			self.walk_angle = self.walk_angle - 5
			self.angle_build = self.angle_build + 5			
		
			if self.angle_build == 30:
				self.angle_build = 0
				self.firstAttackPart = True
		
		# Attack swing back 
		if self.firstAttackPart == True and self.secondAttackPart == False:
			self.walk_angle = self.walk_angle + 5
			self.angle_build = self.angle_build + 5
			
			if self.angle_build == 30:
				self.secondAttackPart = True
		
        # Attack sequence complete
		if self.firstAttackPart == True and self.secondAttackPart == True:
			self.firstAttackPart = False
			self.secondAttackPart = False
			self.angle_build = 0
			self.attack = False
			self.noOfAttacks = self.noOfAttacks + 1
	
	# Setup detection zone around character
	def setupDetectionZone(self):
		self.area_xpos = (self.x - 100)
		self.area_ypos = (self.y - 100)
		self.area_xlength = 200
		self.area_ylength = 200
	
	# Display AI Player status
	def displayStatus(self, screenIn, pxIn, pyIn):
		self.testtext = create_text(str(self.name), 22, (0, 128, 0))
		self.player_life = create_text(str(self.energy), 22, (0, 128, 0))		

		# Output Player statistics 
		screenIn.blit(player_stats, (round((pxIn+300)), round((pyIn-400))))
		screenIn.blit(heart_icon, (round((pxIn+310)), round((pyIn-350))))		
		screenIn.blit(self.player_life, (round((pxIn+360)), round((pyIn-350))))	
		screenIn.blit(self.testtext, (round((pxIn+310)), round((pyIn-400))))	
		
##########	PLAYER / CHARACTER CREATION	  ##############

# Create a human player
humanDwarf = DwarfPlayer('Andrew')

# Create an AI dwawf player
aiDwarfCollection = [ ]
aiDwarfCollection.append(DwarfAIPlayer('Ronald')) # Playroom 
aiDwarfCollection.append(DwarfAIPlayer('Donald')) # Hallway 2
aiDwarfCollection.append(DwarfAIPlayer('Murphy')) # Throne Room Enemy Dwarf 1
aiDwarfCollection.append(DwarfAIPlayer('Lewis')) # Throne Room Enemy Dwarf 2
aiDwarfCollection.append(DwarfAIPlayer('Tom')) # Gala Room Enemy Dwarf 1
aiDwarfCollection.append(DwarfAIPlayer('Jerry')) # Gala Room Enemy Dwarf 2
aiDwarfCollection.append(DwarfAIPlayer('Tango')) # Treasure Hallway (left-side) Enemy Dwarf 1
aiDwarfCollection.append(DwarfAIPlayer('Cash')) # Treasure Hallway (left-side) Enemy Dwarf 2
aiDwarfCollection.append(DwarfAIPlayer('Gerald')) # Hallway Two Enemy Dwarf 1

# Set-up the Dwarf called 'Ronald'

aiDwarfCollection[0].x = 500
aiDwarfCollection[0].y = 500

aiDwarfCollection[1].x = 1400
aiDwarfCollection[1].y = 500

aiDwarfCollection[2].x = 1500
aiDwarfCollection[2].y = 700

aiDwarfCollection[3].x = 1500
aiDwarfCollection[3].y = 1200

aiDwarfCollection[4].x = 1500
aiDwarfCollection[4].y = 2600

aiDwarfCollection[5].x = 1500
aiDwarfCollection[5].y = 2700

aiDwarfCollection[6].x = -600
aiDwarfCollection[6].y = 2400

aiDwarfCollection[7].x = -600
aiDwarfCollection[7].y = 2700

aiDwarfCollection[8].x = -100
aiDwarfCollection[8].y = 450

aiDwarfCollection[0].walk_angle = 180
aiDwarfCollection[0].walk_target_angle = 170

aiDwarfCollection[1].walk_angle = -90
aiDwarfCollection[1].walk_target_angle -80

aiDwarfCollection[2].walk_angle = -90
aiDwarfCollection[2].walk_target_angle = -80

aiDwarfCollection[3].walk_angle = -270
aiDwarfCollection[3].walk_target_angle = -260

# Setup Detection Zone around enemy Dwarf
aiDwarfCollection[0].setupDetectionZone()
aiDwarfCollection[0].direction_indicator = DOWN_DIRECTION

aiDwarfCollection[1].setupDetectionZone()
aiDwarfCollection[1].direction_indicator = RIGHT_DIRECTION

aiDwarfCollection[2].setupDetectionZone()
aiDwarfCollection[2].direction_indicator = RIGHT_DIRECTION

aiDwarfCollection[3].setupDetectionZone()
aiDwarfCollection[3].direction_indicator = LEFT_DIRECTION

aiDwarfCollection[4].setupDetectionZone()
aiDwarfCollection[4].direction_indicator = LEFT_DIRECTION

aiDwarfCollection[5].setupDetectionZone()
aiDwarfCollection[5].direction_indicator = UP_DIRECTION

aiDwarfCollection[6].setupDetectionZone()
aiDwarfCollection[6].direction_indicator = UP_DIRECTION

aiDwarfCollection[7].setupDetectionZone()
aiDwarfCollection[7].direction_indicator = LEFT_DIRECTION

aiDwarfCollection[8].setupDetectionZone()
aiDwarfCollection[8].direction_indicator = LEFT_DIRECTION

# Used to create text to output to PyGame screen
def create_text(text, size, color):
	# Set the font to be used	
	font = pygame.font.SysFont('Comic Sans MS', size)
	
	# Get as image to be shown on screen
	image = font.render(text, True, color)

	return image

# Set screen size / interface
screen = pygame.display.set_mode((HORIZ_RESOLUTION, VERT_RESOLUTION))

pygame.display.set_caption('')
clock = pygame.time.Clock()

# Black coloured screen	
screen.fill((0, 0, 0))	

###################################
########   Load Images	  #########
###################################

# Game Over - Win image
try:
	gameover_win = pygame.image.load('../images/misc/gameover_win.jpg').convert()
except:
	pygame.quit()
	print('Game Win Image Missing....gameover_win.jpg')
	sleep(5)
	
try:
	gameover_loose = pygame.image.load('../images/misc/gameover_loose.jpg').convert()
except:
	pygame.quit()
	print('Game Loose image missing...gameover_loose.jpg')
	sleep(5)


# Background image 
try:
	background_image = pygame.image.load('../images/Background/frosty.jpg').convert()
except:
	pygame.quit()
	print('Background Image Missing...frosty.jpg...exiting program')
	sleep(5)
	

# Load Player Image (Front facing with axe)
try:
	playerImageFront01 = pygame.image.load('../images/GameCharacter/Dwarf/Good/dwarffront01.png').convert()
except:
	pygame.quit()
	print('Player Image Missing...dwarffront01.png...exiting program')
	sleep(5)
	
# Get the alpha colour to be transparent
transColor = playerImageFront01.get_at((0, 0))
playerImageFront01.set_colorkey(transColor)

# Load empty hand dward image
try:
	empty_dwarf = pygame.image.load('../images/GameCharacter/Dwarf/Good/dwarf-free.png').convert()
except:
	pygame.quit()
	print('Player Image Missing...dwarf-free.png...exiting program')
	sleep(5)
	
empty_dwarf.set_colorkey(transColor)

# Load full armed dwarf image 
try:
	fullarmeddwarf = pygame.image.load('../images/GameCharacter/Dwarf/Good/dwarf-axe-sheild.png').convert()
except:
	pygame.quit()
	print('Player Image Missing...dwarf-axe-sheild.png...exiting program')
	sleep(5)
fullarmeddwarf.set_colorkey(transColor)

# ENEMY IMAGES
# Get Enemy Dwarf Image
try:
	enemyDwarf01 = pygame.image.load('../images/GameCharacter/Dwarf/Bad/enemydwarf.png').convert()
except:
	pygame.quit()
	print('Enemy Image Missing...enemydwarf.png...exiting program')
	sleep(5)

eDwarfTransColor = enemyDwarf01.get_at((0, 0))
enemyDwarf01.set_colorkey(eDwarfTransColor)

# MISC IMAGES
# Load heart icon to represent life level
try:
	heart_icon = pygame.image.load('../images/misc/heart.bmp').convert()
except:
	pygame.quit()
	print('Misc Image Missing...heart.bmp...exiting program')
	sleep(5)
	
# Load gold icon
try:
	gold_icon = pygame.image.load('../images/misc/gold.bmp').convert()
except:
	pygame.quit()
	print('Misc Image Missing...gold.bmp...exiting program')
	sleep(5)
	
# Player details slab
try:
	player_stats = pygame.image.load('../images/misc/gameinfo.bmp').convert()
except:
	pygame.quit()
	print('Misc Image Missing...gameinfo.bmp...exiting program')
	sleep(5)
# GAME OBJECT IMAGES (Box crates, tables, etc...)

# Load Box crate image / object
try:
	boxCrate = pygame.image.load('../images/GameObjects/boxcr.png').convert()
except:
	pygame.quit()
	print('Game Object Image Missing...boxcr.png...exiting program')
	sleep(5)
	
	
# Load Dwaf object images (axe, shield)
try:
	axeimage = pygame.image.load('../images/GameObjects/axeobject.bmp').convert()
except:
	pygame.quit()
	print('Game Object Image Missing...axeobject.bmp...exiting program')
	sleep(5)
	
try:
	shieldimage = pygame.image.load('../images/GameObjects/shieldobject.bmp').convert()
except:
	pygame.quit()
	print('Game Object Missing...shieldobject.bmp...exiting program')
	sleep(5)

# DOOR IMAGES (Vertical and Horizontal)

# Load vertical door image
try:
	vertDoor = pygame.image.load('../images/door/Vertical/doorvert.png').convert()
except:
	pygame.quit()
	print('Door Image Missing...doorvert.png...exiting program')
	sleep(5)
# Load horizontal door image
try:
	horizDoor = pygame.image.load('../images/door/Horizontal/doorhoriz.png').convert()
except:
	pygame.quit()
	print('Door Image Missing...doorhoriz.png...exiting program')
	sleep(5)


# OUTSIDE BRICK IMAGES 

# Load outside brick stack image
try:
	outsideBrickVert1 = pygame.image.load('../images/Bricks/Vertical/outbrickVert1.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert1.jpg...exiting program')
	sleep(5)

# Load outside brick (3 brick vertical)
try:
	outsideBrickVert3 = pygame.image.load('../images/Bricks/Vertical/outbrickVert3.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert3.jpg...exiting program')
	sleep(5)
	
# Load outside brick (21 brick vertical)
try:
	outsideBrickVert21 = pygame.image.load('../images/Bricks/Vertical/outbrickVert21.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert21.jpg...exiting program')
	sleep(5)

# Load outside brick (15 brick vertical)
try:
	outsideBrickVert15 = pygame.image.load('../images/Bricks/Vertical/outbrickVert15.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert15.jpg...exiting program')
	sleep(5)
	
# Load outside brick (16 brick vertical)
try:
	outsideBrickVert16 = pygame.image.load('../images/Bricks/Vertical/outbrickVert16.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert16.jpg...exiting program')
	sleep(5)
	
# Load outside brick (5 brick vertical)
try:
	outsideBrickVert5 = pygame.image.load('../images/Bricks/Vertical/outbrickVert5.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert5.jpg...exiting program')
	sleep(5)
	
# Load outside brick (8 brick vertical)
try:
	outsideBrickVert8 = pygame.image.load('../images/Bricks/Vertical/outbrickVert8.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickVert8.jpg...exiting program')
	sleep(5)

# Load outside brick stage image (Horizontal)
try:
	outsideBrickHoriz1 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz1.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz1.jpg...exiting program')
	sleep(5)
	
# Load outside brick (7 brick horizontal)
try:
	outsideBrickHoriz7 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz7.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz7.jpg...exiting program')
	sleep(5)
	
try:
	outsideBrickHoriz7a = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz7a.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz7a.jpg...exiting program')
	sleep(5)
	
# Load outside brick (3 brick horizontal)
try:
	outsideBrickHoriz3 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz3.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz3.jpg...exiting program')
	sleep(5)
	
# Load outside brick (30 horizontal)
try:
	outsideBrickHoriz30 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz30.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz30.jpg...exiting program')
	sleep(5)
	
# Load outside brick (20 horizontal)
try:
	outsideBrickHoriz20 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz20.jpg')
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz20.jpg...exiting program')
	sleep(5)
	
# Load outside brick (5 horizontal)
try:
	outsideBrickHoriz5 = pygame.image.load('../images/Bricks/Horizontal/outbrickHoriz5.jpg').convert()
except:
	pygame.quit()
	print('Brick Image Missing...outbrickHoriz5.jpg...exiting program')
	sleep(5)
# ROOM FLOOR TEXTURE IMAGES

# Playroom floor layout
try:
	playroom_floor = pygame.image.load('../images/FloorLayout/PlayRoom/playroom_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...playroom_floor.jpg...exiting program')
	sleep(5)
	
# Hallway Two Floor Layout
try:
	halltwo_floor = pygame.image.load('../images/FloorLayout/HallTwo/halltwo_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...halltwo_floor.jpg...exiting program')
	sleep(5)
	
# Throne Room Floor Layout
try:
	throneroom_floor = pygame.image.load('../images/FloorLayout/ThroneRoom/throneroom_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...throneroom_floor.jpg...exiting program')
	sleep(5)
	
# Throne Hallway Floor Layout
try:
	thronehall_floor = pygame.image.load('../images/FloorLayout/ThroneHall/thronehall_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...thronehall_floor.jpg...exiting program')
	sleep(5)
	
# Hallway One Floor Layout
try:
	hallone_floor = pygame.image.load('../images/FloorLayout/HallOne/hallone_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...hallone_floor.jpg...exiting program')
	sleep(5)
	
# Hallway One B Floor Layout
try:
	halloneb_floor = pygame.image.load('../images/FloorLayout/HallOneB/halloneb_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...halloneb_floor.jpg...exiting program')
	sleep(5)
	
# Treasure Room Floor Layout
try:
	treasureroom_floor = pygame.image.load('../images/FloorLayout/TreasureRoom/treasureroom_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...treasureroom_floor.jpg...exiting program')
	sleep(5)
	
# Treasure Hall Floor Layout
try:
	treasurehall_floor = pygame.image.load('../images/FloorLayout/TreasureHall/treasurehall_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...treasurehall_floor.jpg...exiting program')
	sleep(5)
# Gala Hall Floor Layout
try:
	galahall_floor = pygame.image.load('../images/FloorLayout/GalaHall/galahall_floor.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...galahall_floor.jpg...exiting program')
	sleep(5)
	
# Load hall connection Layout
try:
	hallConnection = pygame.image.load('../images/FloorLayout/HallConnection/hallconnection.jpg').convert()
except:
	pygame.quit()
	print('Floor Image Missing...hallconnection.jpg...exiting program')
	sleep(5)
	
hallConnection.set_colorkey(transColor)


#############################################
##########	  DOOR POSITION VARIABLES  ######
#############################################

# Door to left of playroom
door_x1_playroom = 175
door_y1_playroom = 400
	
# Door to right of playroom
door_x2_playroom = 975
door_y2_playroom = 400

# Treasure room entry door
door_x1_treasure = -750
door_y1_treasure = 1075

# Treasure room exit door
door_x2_treasure = -750
door_y2_treasure = 1475

# Throne room door 1
door_x1_throne = 1550
door_y1_throne = 525

# Throne room door 2
door_x2_throne = 1550
door_y2_throne = 1325

# Gala Room Door 1 (Horizontal door image) 
door_x1_gala = 1550
door_y1_gala = 2325

# Gala Room Door 2 (Vertical door image)
door_x2_gala = 1175
door_y2_gala = 2650

#########################################################
#####  Playroom Brick variables	  #######################
#########################################################

playroom_b_left_upper_x = 200
playroom_b_left_upper_y = 7
	
playroom_b_left_lower_x = 200
playroom_b_left_lower_y = 500

playroom_b_right_upper_x = 950
playroom_b_right_upper_y = 7
	
playroom_b_right_lower_x = 950
playroom_b_right_lower_y = 500

playroom_b_bottom_x = 250
playroom_b_bottom_y = 850

playroom_b_top_x = 250
playroom_b_top_y = 0

#######################################################
###	 Hallway 2 brick variables	 ######################
#######################################################

hallwaytwo_b_top_x = 1050
hallwaytwo_b_top_y = 300

hallwaytwo_b_bottom_x = 1050
hallwaytwo_b_bottom_y = 550

hallwaytwo_b_leftdoor_x = 1400
hallwaytwo_b_leftdoor_y = 550

hallwaytwo_b_rightdoor_x = 1650
hallwaytwo_b_rightdoor_y = 550

hallwaytwothrone_b_rightwall_x = 1800
hallwaytwothrone_b_rightwall_y = 350

######################################################
###	  THRONE_ROOM brick variables	  ################
######################################################

throneroom_b_leftdoor_x = 1400
throneroom_b_leftdoor_y = 1300

throneroom_b_rightdoor_x = 1650
throneroom_b_rightdoor_y = 1300

throneroom_b_leftwall_x = 1350
throneroom_b_leftwall_y = 600

######################################################
#######	   THRONE_HALLWAY brick variables	 #########
######################################################

thronehall_b_leftwall_x = 1450
thronehall_b_leftwall_y = 1355

thronehall_b_rightwall_x = 1700
thronehall_b_rightwall_y = 1355

######################################################
#########	GALA ROOM brick variables	 #############
######################################################

galaroom_b_rightwall_x = 2000
galaroom_b_rightwall_y = 2400

galaroom_b_bottomwall_x = 1200
galaroom_b_bottomwall_y = 3150

galaroom_b_tdoor_right_x = 1650
galaroom_b_tdoor_right_y = 2350

galaroom_b_tdoor_left_x = 1200
galaroom_b_tdoor_left_y = 2350

galaroom_b_sdoor_left_x = 1200
galaroom_b_sdoor_left_y = 2400
	
galaroom_b_sdoor_right_x = 1200
galaroom_b_sdoor_right_y = 2750

######################################################
############	GALA_HALLWAY Brick variables  ########
######################################################

galahall_b_top_x = -300
galahall_b_top_y = 2550

galahall_b_bottom_x = -300
galahall_b_bottom_y = 2800

#######################################################
##########	 TREASURE_ROOM Brick variables	 ##########
#######################################################

treasureroom_b_upright_x = -650
treasureroom_b_upright_y = 1050

treasureroom_b_rightw_x = -500
treasureroom_b_rightw_y = 1100

treasureroom_b_leftw_x = -950
treasureroom_b_leftw_y = 1100

#######################################################
############   HALLWAY_ONEB Brick Variables	  #########
#######################################################

hallwayoneb_b_rwall_x = -600
hallwayoneb_b_rwall_y = 550

hallwayoneb_b_lwall_x = -850
hallwayoneb_b_lwall_y = 350

#######################################################
###########	  HALLWAY_ONE Brick variables	###########
#######################################################

hallwayone_b_twall_x = -800
hallwayone_b_twall_y = 300

hallwayone_b_bwall_x = -600
hallwayone_b_bwall_y = 550

#######################################################
############  Hallway Connection Brick variables  #####
#######################################################

hallconn_b_bottom_x = -1100
hallconn_b_bottom_y = 2800

hallconn_b_left_x = -1100
hallconn_b_left_y = 2000

hallconn_b_righth_x = -550
hallconn_b_righth_y = 2450

hallconn_b_lefth_x = -1100
hallconn_b_lefth_y = 2000

hallconn_b_leftv_x = -800
hallconn_b_leftv_y = 1600

#############################################
########   FLOOR POSITION VARIABLES	  #######
#############################################

# Hall connection floor variables
hallconnection_x = -1095
hallconnection_y = 2050

# Playroom floor variables
playroom_floor_x = 200
playroom_floor_y = 50

# Hallway Two Floor variables
halltwo_floor_x = 1000
halltwo_floor_y = 350

# Throne Room Floor variables
throneroom_floor_x = 1400
throneroom_floor_y = 550

# Throne Hallway variables
thronehall_floor_x = 1500
thronehall_floor_y = 1350

# Gala Room Floor variables
galaroom_floor_x = 1200
galaroom_floor_y = 2350

# Hallway One Floor variables
hallone_floor_x = -600
hallone_floor_y = 350

# Hallway One-B Floor variables
halloneb_floor_x = -800
halloneb_floor_y = 350

# Treasure Room Floor variables
treasureroom_floor_x = -900
treasureroom_floor_y = 1100

# Treasure Hallway Floor variables
treasurehall_floor_x = -750
treasurehall_floor_y = 1500

# Gala Hall Floor variables
galahall_floor_x = -300
galahall_floor_y = 2600

##############################################
####	PROGRAM CONTROL VARIABLES	##########
##############################################

# Set program end flag to False (Default)
programEnd = False

# Room Control Variables (Render Control)
# Flags to identify when to show areas of the game
showPlayroom = True
showHallwayOne = True
showHallWayOneB = True
showHallWayTwo = True
showThroneRoom = True
showThroneHall = True
showTreasureRoom = True
showTreasureHall = True
showGalaRoom = True
showGalaHall = True

##############################################
#######	        GAME OBJECTS	  ############
##############################################

gameObjectCollection = [ ] # Stores game objects 

# Room Description, Object Type, Active / Non Active, X-Position, Y-position
gameObjectCollection.append(['PLAYROOM', 'BOX_CRATE', True, 300, 600])
gameObjectCollection.append(['PLAYROOM', 'BOX_CRATE', True, 300, 200])
gameObjectCollection.append(['PLAYROOM', 'HEART_ICON', True, humanDwarf.x, humanDwarf.y-500])
gameObjectCollection.append(['PLAYROOM', 'DWARF_AXE', True, 600, 600])
gameObjectCollection.append(['THRONE_ROOM', 'DWARF_SHIELD', True, 1400, 1000])
gameObjectCollection.append(['THRONE_HALLWAY', 'HEART_ICON', True, door_x2_throne-50, door_y2_throne+250])


# Render areas of the game depending on what area 
# of the game the human player is in 
def renderGameAreas_OnCondition(roomDescIn):
	global screen
	global playroom_floor_x
	global playroom_floor_y
	global halltwo_floor_x
	global halltwo_floor_y
	global galaroom_floor_x
	global galaroom_floor_y
	
	# Flags to identify when to show areas of the game
	global showPlayroom
	global showHallwayOne
	global showHallWayOneB
	global showHallWayTwo
	global showThroneRoom
	global showThroneHall
	global showGalaRoom
	global showGalaHall
	global showTreasureRoom
	global showTreasureHall
	
	if roomDescIn == 'PLAYROOM':
		showPlayroom = True
		showHallWayTwo = True
		showThroneRoom = True
		showHallwayOne = True
		
		showHallWayOneB = False
		showThroneHall = False
		showGalaRoom = False
		showGalaHall = False
		showTreasureRoom = False
		showTreasureHall = False
		
	if roomDescIn == 'HALLWAY_TWO':
		showPlayroom = True
		showHallWayTwo = True
		showThroneRoom = True
		
		showHallWayOneB = False
		showThroneHall = False
		showGalaRoom = False
		showGalaHall = False
		showTreasureRoom = False
		showTreasureHall = False
		
	if roomDescIn == 'THRONE_ROOM':
		showPlayroom = True
		showHallWayTwo = True
		showThroneRoom = True
		showThroneHall = True
		
		showHallWayOneB = False
		showHallwayOne = False
		showGalaRoom = False
		showGalaHall = False
		showTreasureRoom = False
		showTreasureHall = False
		
	if roomDescIn == 'THRONE_HALLWAY':
		showThroneRoom = True
		showThroneHall = True
		showGalaRoom = True
		showGalaHall = True
		
		showPlayroom = False
		showHallwayOne = False
		showHallWayOneB = False
		showTreasureHall = False
		showTreasureRoom = False
		
	if roomDescIn == 'GALA_ROOM':
		showThroneHall = True
		showGalaRoom = True
		showGalaHall = True
		
		showThroneRoom = False
		showHallWayTwo = False
		showPlayroom = False
		showHallwayOne = False
		showHallWayOneB = False
		showTreasureHall = False
		
	if roomDescIn == 'GALA_HALLWAY':
		showGalaHall = True
		showGalaRoom = True
		showThroneHall = True
		showTreasureHall= True
		
		showTreasureRoom = False
		showHallWayOneB = False
		showHallwayOne = False
		showHallWayTwo = False
		showThroneRoom = False
		
	if roomDescIn == 'TREASURE_HALLWAY':
		showTreasureRoom = True
		showTreasureHall = True
		showGalaHall = True
		showHallWayOneB = True
		
		showGalaRoom = False
		showThroneHall = False
		showThroneRoom = False
		showHallWayTwo = False
		showPlayroom = False
		showHallwayOne = False
		
	if roomDescIn == 'TREASURE_ROOM':
		showTreasureRoom = True
		showTreasureHall = True
		showGalaHall = True
		showHallWayOneB = True
		
		showHallwayOne = False
		showPlayroom = False
		showHallWayTwo = False
		showThroneRoom = False
		showThroneHall = False
		showGalaRoom = False
		
	if roomDescIn == 'HALLWAY_ONEB':
		showHallWayOneB = True
		showTreasureRoom = True
		showHallwayOne = True
		showPlayroom = True
		
		showHallWayTwo = False
		showThroneRoom = False
		showThroneHall = False
		showGalaRoom = False
		showGalaHall = False
		showTreasureHall = False
		
	if roomDescIn == 'HALLWAY_ONE':
		showHallWayOneB = True
		showHallwayOne = True
		showPlayroom = True
		
		showTreasureRoom = False
		showTreasureHall = False
		showGalaHall = False
		showGalaRoom = False
		showThroneHall = False
		showThroneRoom = False
		showHallWayTwo = False
		
	
	# If the Playroom is active then do the following.....
	if showPlayroom == True:		
		# Playroom floor	
		screen.blit(playroom_floor, (playroom_floor_x,playroom_floor_y))
		
	if showHallWayTwo == True:	
		# Hall Two floor	
		screen.blit(halltwo_floor, (halltwo_floor_x, halltwo_floor_y))		
	
	if showThroneRoom == True:			
		# Throne Room Floor
		screen.blit(throneroom_floor, (throneroom_floor_x, throneroom_floor_y))		
	
	if showThroneHall == True:	
		# Throne Hall Way
		screen.blit(thronehall_floor, (thronehall_floor_x, thronehall_floor_y))		
		
	if showGalaRoom == True:	
		# Gala Room
		screen.blit(playroom_floor, (galaroom_floor_x, galaroom_floor_y))		
	
	if showGalaHall == True:	
		# Gala Hallway
		screen.blit(galahall_floor, (galahall_floor_x, galahall_floor_y))
		screen.blit(hallConnection, (hallconnection_x, hallconnection_y))
	
	if showHallwayOne == True:	
		# Hallway One
		screen.blit(hallone_floor, (hallone_floor_x, hallone_floor_y))
	
	if showHallWayOneB == True:	
		# Hallway One-B
		screen.blit(halloneb_floor, (halloneb_floor_x, halloneb_floor_y))
	
	if showTreasureRoom == True:	
		# Treasure Room
		screen.blit(treasureroom_floor, (treasureroom_floor_x, treasureroom_floor_y))
			
	if showTreasureHall == True:	
		# Treasure Hallway
		screen.blit(treasurehall_floor, (treasurehall_floor_x, treasurehall_floor_y))


#######################		GAME ENVIRONMENT MOVEMENT OPERATIONS		############################################

def moveFloorDown():
	global door_y1_playroom
	global door_y2_playroom
	global door_y1_treasure
	global door_y2_treasure
	global door_y1_throne
	global door_y2_throne
	global door_y1_gala
	global door_y2_gala
	
	global playroom_b_left_upper_y
	global playroom_b_left_lower_y
	global playroom_b_right_upper_y
	global playroom_b_right_lower_y
	global playroom_b_bottom_y
	global playroom_b_top_y
	
	global hallwaytwo_b_top_y
	global hallwaytwo_b_bottom_y
	global hallwaytwo_b_leftdoor_y
	global hallwaytwo_b_rightdoor_y
	global hallwaytwothrone_b_rightwall_y
	global throneroom_b_leftdoor_y
	global throneroom_b_rightdoor_y
	global throneroom_b_leftwall_y
	global thronehall_b_leftwall_y
	global thronehall_b_rightwall_y
	global galaroom_b_rightwall_y
	global galaroom_b_bottomwall_y
	global galaroom_b_tdoor_right_y
	global galaroom_b_tdoor_left_y
	global galaroom_b_sdoor_left_y
	global galaroom_b_sdoor_right_y
	
	global galahall_b_top_y
	global galahall_b_bottom_y
	
	global hallconn_b_bottom_y
	global hallconn_b_left_y
	global hallconn_b_righth_y
	global hallconn_b_lefth_y
	global hallconn_b_leftv_y
	
	global treasureroom_b_upright_y
	global treasureroom_b_rightw_y
	global treasureroom_b_leftw_y
	
	global hallwayoneb_b_rwall_y
	global hallwayoneb_b_lwall_y
	
	global hallwayone_b_twall_y
	global hallwayone_b_bwall_y
	
	global playroom_floor_y
	global halltwo_floor_y
	global throneroom_floor_y
	global thronehall_floor_y
	global galaroom_floor_y
	global hallone_floor_y
	global halloneb_floor_y
	global treasureroom_floor_y
	global treasurehall_floor_y
	global galahall_floor_y
	
	global hallconnection_y
	
	global aiDwarfCollection

	icount = 0
	movespeed = 4
	
	# Move the game objects in the game along with the map
	cCounter = 0
	
	while cCounter < len(gameObjectCollection):
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'BOX_CRATE':
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'DWARF_AXE' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_ROOM' and gameObjectCollection[cCounter][1] == 'DWARF_SHIELD' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_HALLWAY' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] + movespeed
			
		cCounter = cCounter + 1
		
	door_y1_playroom = door_y1_playroom + movespeed
	door_y2_playroom = door_y2_playroom + movespeed
	door_y1_treasure = door_y1_treasure + movespeed
	door_y2_treasure = door_y2_treasure + movespeed
	door_y1_throne = door_y1_throne + movespeed
	door_y2_throne = door_y2_throne + movespeed
	door_y1_gala = door_y1_gala + movespeed
	door_y2_gala = door_y2_gala + movespeed
	
	playroom_b_left_upper_y = playroom_b_left_upper_y + movespeed
	playroom_b_left_lower_y = playroom_b_left_lower_y + movespeed
	playroom_b_right_upper_y = playroom_b_right_upper_y + movespeed
	playroom_b_right_lower_y = playroom_b_right_lower_y + movespeed
	playroom_b_bottom_y = playroom_b_bottom_y + movespeed
	playroom_b_top_y = playroom_b_top_y + movespeed
	
	hallwaytwo_b_top_y = hallwaytwo_b_top_y + movespeed
	hallwaytwo_b_bottom_y = hallwaytwo_b_bottom_y + movespeed
	hallwaytwo_b_leftdoor_y = hallwaytwo_b_leftdoor_y  + movespeed
	hallwaytwo_b_rightdoor_y = hallwaytwo_b_rightdoor_y + movespeed
	hallwaytwothrone_b_rightwall_y = hallwaytwothrone_b_rightwall_y + movespeed
	throneroom_b_leftdoor_y = throneroom_b_leftdoor_y + movespeed
	throneroom_b_rightdoor_y = throneroom_b_rightdoor_y + movespeed
	throneroom_b_leftwall_y = throneroom_b_leftwall_y + movespeed
	thronehall_b_leftwall_y = thronehall_b_leftwall_y + movespeed
	thronehall_b_rightwall_y = thronehall_b_rightwall_y + movespeed
	galaroom_b_rightwall_y = galaroom_b_rightwall_y + movespeed
	galaroom_b_bottomwall_y = galaroom_b_bottomwall_y + movespeed
	galaroom_b_tdoor_right_y = galaroom_b_tdoor_right_y + movespeed
	galaroom_b_tdoor_left_y = galaroom_b_tdoor_left_y + movespeed
	galaroom_b_sdoor_left_y = galaroom_b_sdoor_left_y + movespeed
	galaroom_b_sdoor_right_y = galaroom_b_sdoor_right_y + movespeed
	galahall_b_top_y = galahall_b_top_y + movespeed
	galahall_b_bottom_y = galahall_b_bottom_y + movespeed
	hallconn_b_bottom_y = hallconn_b_bottom_y + movespeed
	hallconn_b_left_y = hallconn_b_left_y + movespeed
	hallconn_b_righth_y = hallconn_b_righth_y + movespeed
	hallconn_b_lefth_y = hallconn_b_lefth_y + movespeed
	hallconn_b_leftv_y = hallconn_b_leftv_y + movespeed
	treasureroom_b_upright_y = treasureroom_b_upright_y + movespeed
	treasureroom_b_rightw_y = treasureroom_b_rightw_y + movespeed
	treasureroom_b_leftw_y = treasureroom_b_leftw_y + movespeed
	hallwayoneb_b_rwall_y = hallwayoneb_b_rwall_y + movespeed
	hallwayoneb_b_lwall_y = hallwayoneb_b_lwall_y + movespeed
	hallwayone_b_twall_y = hallwayone_b_twall_y + movespeed
	hallwayone_b_bwall_y = hallwayone_b_bwall_y + movespeed
	
	playroom_floor_y = playroom_floor_y + movespeed
	halltwo_floor_y = halltwo_floor_y + movespeed
	throneroom_floor_y = throneroom_floor_y + movespeed
	thronehall_floor_y = thronehall_floor_y + movespeed
	galaroom_floor_y = galaroom_floor_y + movespeed
	hallone_floor_y = hallone_floor_y + movespeed
	halloneb_floor_y = halloneb_floor_y + movespeed
	treasureroom_floor_y = treasureroom_floor_y + movespeed
	treasurehall_floor_y = treasurehall_floor_y + movespeed
	galahall_floor_y = galahall_floor_y + movespeed
	
	hallconnection_y = hallconnection_y + movespeed
	
	# Check to see if there are enemy dwarf characters to process
	if len(aiDwarfCollection) > 0:
		dwcount = 0
		for enemydwarf in aiDwarfCollection:
			aiDwarfCollection[dwcount].y = aiDwarfCollection[dwcount].y + movespeed
			aiDwarfCollection[dwcount].area_ypos = aiDwarfCollection[dwcount].area_ypos + movespeed
			dwcount = dwcount + 1
		
def moveFloorUp():
	global door_y1_playroom
	global door_y2_playroom
	global door_y1_treasure
	global door_y2_treasure
	global door_y1_throne
	global door_y2_throne
	global door_y1_gala
	global door_y2_gala
	
	global playroom_b_left_upper_y
	global playroom_b_left_lower_y
	global playroom_b_right_upper_y
	global playroom_b_right_lower_y
	global playroom_b_bottom_y
	global playroom_b_top_y
	
	global hallwaytwo_b_top_y
	global hallwaytwo_b_bottom_y
	global hallwaytwo_b_leftdoor_y
	global hallwaytwo_b_rightdoor_y
	global hallwaytwothrone_b_rightwall_y
	global throneroom_b_leftdoor_y
	global throneroom_b_rightdoor_y
	global throneroom_b_leftwall_y
	global thronehall_b_leftwall_y
	global thronehall_b_rightwall_y
	global galaroom_b_rightwall_y
	global galaroom_b_bottomwall_y
	global galaroom_b_tdoor_right_y
	global galaroom_b_tdoor_left_y
	global galaroom_b_sdoor_left_y
	global galaroom_b_sdoor_right_y
	global galahall_b_top_y
	global galahall_b_bottom_y
	global hallconn_b_bottom_y
	global hallconn_b_left_y
	global hallconn_b_righth_y
	global hallconn_b_lefth_y
	global hallconn_b_leftv_y
	global treasureroom_b_upright_y
	global treasureroom_b_rightw_y
	global treasureroom_b_leftw_y
	global hallwayoneb_b_rwall_y
	global hallwayoneb_b_lwall_y
	global hallwayone_b_twall_y
	global hallwayone_b_bwall_y
	
	global playroom_floor_y
	global halltwo_floor_y
	global throneroom_floor_y
	global thronehall_floor_y
	global galaroom_floor_y
	global hallone_floor_y
	global halloneb_floor_y
	global treasureroom_floor_y
	global treasurehall_floor_y
	global galahall_floor_y
	
	global hallconnection_y
	
	global aiDwarfCollection

	icount = 0
	movespeed = 4
	
	# Move the game objects in the game along with the map
	cCounter = 0
	
	while cCounter < len(gameObjectCollection):
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'BOX_CRATE':
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'DWARF_AXE' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_ROOM' and gameObjectCollection[cCounter][1] == 'DWARF_SHIELD' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_HALLWAY' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][4] = gameObjectCollection[cCounter][4] - movespeed
			
		cCounter = cCounter + 1
		
	door_y1_playroom = door_y1_playroom - movespeed
	door_y2_playroom = door_y2_playroom - movespeed
	door_y1_treasure = door_y1_treasure - movespeed
	door_y2_treasure = door_y2_treasure - movespeed
	door_y1_throne = door_y1_throne - movespeed
	door_y2_throne = door_y2_throne - movespeed
	door_y1_gala = door_y1_gala - movespeed
	door_y2_gala = door_y2_gala - movespeed
	
	playroom_b_left_upper_y = playroom_b_left_upper_y - movespeed
	playroom_b_left_lower_y = playroom_b_left_lower_y - movespeed
	playroom_b_right_upper_y = playroom_b_right_upper_y - movespeed
	playroom_b_right_lower_y = playroom_b_right_lower_y - movespeed
	playroom_b_bottom_y = playroom_b_bottom_y - movespeed
	playroom_b_top_y = playroom_b_top_y - movespeed
	
	hallwaytwo_b_top_y = hallwaytwo_b_top_y - movespeed
	hallwaytwo_b_bottom_y = hallwaytwo_b_bottom_y - movespeed
	hallwaytwo_b_leftdoor_y = hallwaytwo_b_leftdoor_y - movespeed
	hallwaytwo_b_rightdoor_y = hallwaytwo_b_rightdoor_y - movespeed
	hallwaytwothrone_b_rightwall_y = hallwaytwothrone_b_rightwall_y - movespeed
	throneroom_b_leftdoor_y = throneroom_b_leftdoor_y - movespeed
	throneroom_b_rightdoor_y = throneroom_b_rightdoor_y - movespeed
	throneroom_b_leftwall_y = throneroom_b_leftwall_y - movespeed
	thronehall_b_leftwall_y = thronehall_b_leftwall_y - movespeed
	thronehall_b_rightwall_y = thronehall_b_rightwall_y - movespeed
	galaroom_b_rightwall_y = galaroom_b_rightwall_y - movespeed
	galaroom_b_bottomwall_y = galaroom_b_bottomwall_y - movespeed
	galaroom_b_tdoor_right_y = galaroom_b_tdoor_right_y - movespeed
	galaroom_b_tdoor_left_y = galaroom_b_tdoor_left_y - movespeed
	galaroom_b_sdoor_left_y = galaroom_b_sdoor_left_y - movespeed
	galaroom_b_sdoor_right_y = galaroom_b_sdoor_right_y - movespeed
	galahall_b_top_y = galahall_b_top_y - movespeed
	galahall_b_bottom_y = galahall_b_bottom_y - movespeed
	hallconn_b_bottom_y = hallconn_b_bottom_y - movespeed
	hallconn_b_left_y = hallconn_b_left_y - movespeed
	hallconn_b_righth_y = hallconn_b_righth_y - movespeed
	hallconn_b_lefth_y = hallconn_b_lefth_y - movespeed
	hallconn_b_leftv_y = hallconn_b_leftv_y - movespeed
	treasureroom_b_upright_y = treasureroom_b_upright_y - movespeed
	treasureroom_b_rightw_y = treasureroom_b_rightw_y - movespeed
	treasureroom_b_leftw_y = treasureroom_b_leftw_y - movespeed
	hallwayoneb_b_rwall_y = hallwayoneb_b_rwall_y - movespeed
	hallwayoneb_b_lwall_y = hallwayoneb_b_lwall_y - movespeed
	hallwayone_b_twall_y = hallwayone_b_twall_y - movespeed
	hallwayone_b_bwall_y = hallwayone_b_bwall_y - movespeed
	
	playroom_floor_y = playroom_floor_y - movespeed
	halltwo_floor_y = halltwo_floor_y - movespeed
	throneroom_floor_y = throneroom_floor_y - movespeed
	thronehall_floor_y = thronehall_floor_y - movespeed
	galaroom_floor_y = galaroom_floor_y - movespeed
	hallone_floor_y = hallone_floor_y - movespeed
	halloneb_floor_y = halloneb_floor_y - movespeed
	treasureroom_floor_y = treasureroom_floor_y - movespeed
	treasurehall_floor_y = treasurehall_floor_y - movespeed
	galahall_floor_y = galahall_floor_y - movespeed
	
	hallconnection_y = hallconnection_y - movespeed
	
	if len(aiDwarfCollection) > 0:
		dwcount = 0
		for enemydwarf in aiDwarfCollection:
			aiDwarfCollection[dwcount].y = aiDwarfCollection[dwcount].y - movespeed
			aiDwarfCollection[dwcount].area_ypos = aiDwarfCollection[dwcount].area_ypos - movespeed
			dwcount = dwcount + 1

		
def moveFloorRight():
	global door_x1_playroom
	global door_x2_playroom
	global door_x1_treasure
	global door_x2_treasure
	global door_x1_throne
	global door_x2_throne
	global door_x1_gala
	global door_x2_gala
	
	global playroom_b_left_upper_x
	global playroom_b_left_lower_x
	global playroom_b_right_upper_x
	global playroom_b_right_lower_x
	global playroom_b_bottom_x
	global playroom_b_top_x
	
	global hallwaytwo_b_top_x
	global hallwaytwo_b_bottom_x
	global hallwaytwo_b_leftdoor_x
	global hallwaytwo_b_rightdoor_x
	global hallwaytwothrone_b_rightwall_x
	global throneroom_b_leftdoor_x
	global throneroom_b_rightdoor_x
	global throneroom_b_leftwall_x
	global thronehall_b_leftwall_x
	global thronehall_b_rightwall_x
	global galaroom_b_rightwall_x
	global galaroom_b_bottomwall_x
	global galaroom_b_tdoor_right_x
	global galaroom_b_tdoor_left_x
	global galaroom_b_sdoor_left_x
	global galaroom_b_sdoor_right_x
	global galahall_b_top_x
	global galahall_b_bottom_x
	global hallconn_b_bottom_x
	global hallconn_b_left_x
	global hallconn_b_righth_x
	global hallconn_b_lefth_x
	global hallconn_b_leftv_x
	global treasureroom_b_upright_x
	global treasureroom_b_rightw_x
	global treasureroom_b_leftw_x
	global hallwayoneb_b_rwall_x	
	global hallwayoneb_b_lwall_x
	global hallwayone_b_twall_x
	global hallwayone_b_bwall_x
	
	global playroom_floor_x
	global halltwo_floor_x
	global throneroom_floor_x
	global thronehall_floor_x
	global galaroom_floor_x
	global hallone_floor_x
	global halloneb_floor_x
	global treasureroom_floor_x
	global treasurehall_floor_x
	global galahall_floor_x
	
	global hallconnection_x
	
	global aiDwarfCollection

	icount = 0
	movespeed = 4
	
	# Move the game objects in the game along with the map
	cCounter = 0
	
	while cCounter < len(gameObjectCollection):
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'BOX_CRATE':
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'DWARF_AXE' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_ROOM' and gameObjectCollection[cCounter][1] == 'DWARF_SHIELD' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] + movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_HALLWAY' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] + movespeed
			
		cCounter = cCounter + 1
	
	door_x1_playroom = door_x1_playroom + movespeed
	door_x2_playroom = door_x2_playroom + movespeed
	door_x1_treasure = door_x1_treasure + movespeed
	door_x2_treasure = door_x2_treasure + movespeed
	door_x1_throne = door_x1_throne + movespeed
	door_x2_throne = door_x2_throne + movespeed
	door_x1_gala = door_x1_gala + movespeed
	door_x2_gala = door_x2_gala + movespeed
	
	playroom_b_left_upper_x = playroom_b_left_upper_x + movespeed
	playroom_b_left_lower_x = playroom_b_left_lower_x + movespeed
	playroom_b_right_upper_x = playroom_b_right_upper_x + movespeed
	playroom_b_right_lower_x = playroom_b_right_lower_x + movespeed
	playroom_b_bottom_x = playroom_b_bottom_x + movespeed
	playroom_b_top_x = playroom_b_top_x + movespeed
	
	hallwaytwo_b_top_x = hallwaytwo_b_top_x + movespeed
	hallwaytwo_b_bottom_x = hallwaytwo_b_bottom_x + movespeed
	
	hallwaytwo_b_leftdoor_x = hallwaytwo_b_leftdoor_x + movespeed
	hallwaytwo_b_rightdoor_x = hallwaytwo_b_rightdoor_x + movespeed
	hallwaytwothrone_b_rightwall_x = hallwaytwothrone_b_rightwall_x + movespeed
	throneroom_b_leftdoor_x = throneroom_b_leftdoor_x + movespeed
	throneroom_b_rightdoor_x = throneroom_b_rightdoor_x + movespeed
	throneroom_b_leftwall_x = throneroom_b_leftwall_x + movespeed
	thronehall_b_leftwall_x = thronehall_b_leftwall_x + movespeed
	thronehall_b_rightwall_x = thronehall_b_rightwall_x + movespeed
	galaroom_b_rightwall_x = galaroom_b_rightwall_x + movespeed
	galaroom_b_bottomwall_x = galaroom_b_bottomwall_x + movespeed
	galaroom_b_tdoor_right_x = galaroom_b_tdoor_right_x + movespeed
	galaroom_b_tdoor_left_x = galaroom_b_tdoor_left_x + movespeed
	galaroom_b_sdoor_left_x = galaroom_b_sdoor_left_x + movespeed
	galaroom_b_sdoor_right_x = galaroom_b_sdoor_right_x + movespeed
	galahall_b_top_x = galahall_b_top_x + movespeed
	galahall_b_bottom_x = galahall_b_bottom_x + movespeed
	hallconn_b_bottom_x = hallconn_b_bottom_x + movespeed
	hallconn_b_left_x = hallconn_b_left_x + movespeed
	hallconn_b_righth_x = hallconn_b_righth_x + movespeed
	hallconn_b_lefth_x = hallconn_b_lefth_x + movespeed
	hallconn_b_leftv_x = hallconn_b_leftv_x + movespeed
	treasureroom_b_upright_x = treasureroom_b_upright_x + movespeed
	treasureroom_b_rightw_x = treasureroom_b_rightw_x + movespeed
	treasureroom_b_leftw_x = treasureroom_b_leftw_x + movespeed
	hallwayoneb_b_rwall_x = hallwayoneb_b_rwall_x + movespeed
	hallwayoneb_b_lwall_x = hallwayoneb_b_lwall_x + movespeed
	hallwayone_b_twall_x = hallwayone_b_twall_x + movespeed
	hallwayone_b_bwall_x = hallwayone_b_bwall_x + movespeed
	
	playroom_floor_x = playroom_floor_x + movespeed
	halltwo_floor_x = halltwo_floor_x + movespeed
	throneroom_floor_x = throneroom_floor_x + movespeed
	thronehall_floor_x = thronehall_floor_x + movespeed
	galaroom_floor_x = galaroom_floor_x + movespeed
	hallone_floor_x = hallone_floor_x + movespeed
	halloneb_floor_x = halloneb_floor_x + movespeed
	treasureroom_floor_x = treasureroom_floor_x + movespeed
	treasurehall_floor_x = treasurehall_floor_x + movespeed
	galahall_floor_x = galahall_floor_x + movespeed
	hallconnection_x = hallconnection_x + movespeed
	
	if len(aiDwarfCollection) > 0:
		for enemydwarf in aiDwarfCollection:
			enemydwarf.x = enemydwarf.x + movespeed
			enemydwarf.area_xpos = enemydwarf.area_xpos + movespeed
		
def moveFloorLeft():
	global door_x1_playroom
	global door_x2_playroom
	global door_x1_treasure
	global door_x2_treasure
	global door_x1_throne
	global door_x2_throne
	global door_x1_gala
	global door_x2_gala
	
	global playroom_b_left_upper_x
	global playroom_b_left_lower_x
	global playroom_b_right_upper_x
	global playroom_b_right_lower_x
	global playroom_b_bottom_x
	global playroom_b_top_x
	
	global hallwaytwo_b_top_x
	global hallwaytwo_b_bottom_x
	global hallwaytwo_b_leftdoor_x
	global hallwaytwo_b_rightdoor_x
	global hallwaytwothrone_b_rightwall_x
	global throneroom_b_leftdoor_x
	global throneroom_b_rightdoor_x
	global throneroom_b_leftwall_x
	global thronehall_b_leftwall_x
	global thronehall_b_rightwall_x
	global galaroom_b_rightwall_x
	global galaroom_b_bottomwall_x
	global galaroom_b_tdoor_right_x
	global galaroom_b_tdoor_left_x
	global galaroom_b_sdoor_left_x
	global galaroom_b_sdoor_right_x
	global galahall_b_top_x
	global galahall_b_bottom_x
	global hallconn_b_bottom_x
	global hallconn_b_left_x
	global hallconn_b_righth_x
	global hallconn_b_lefth_x
	global hallconn_b_leftv_x
	global treasureroom_b_upright_x
	global treasureroom_b_rightw_x
	global treasureroom_b_leftw_x
	global hallwayoneb_b_rwall_x
	global hallwayoneb_b_lwall_x
	global hallwayone_b_twall_x
	global hallwayone_b_bwall_x
	
	global playroom_floor_x
	global halltwo_floor_x
	global throneroom_floor_x
	global thronehall_floor_x
	global galaroom_floor_x
	global hallone_floor_x
	global halloneb_floor_x
	global treasureroom_floor_x
	global treasurehall_floor_x
	global galahall_floor_x
	
	global hallconnection_x
	
	global aiDwarfCollection
	
	icount = 0
	movespeed = 4
	
	door_x1_playroom = door_x1_playroom - movespeed
	door_x2_playroom = door_x2_playroom - movespeed
	
	door_x1_treasure = door_x1_treasure - movespeed
	door_x2_treasure = door_x2_treasure - movespeed
	door_x1_throne = door_x1_throne - movespeed
	door_x2_throne = door_x2_throne - movespeed
	door_x1_gala = door_x1_gala - movespeed
	door_x2_gala = door_x2_gala - movespeed
	
	playroom_b_left_upper_x = playroom_b_left_upper_x - movespeed
	playroom_b_left_lower_x = playroom_b_left_lower_x - movespeed
	playroom_b_right_upper_x = playroom_b_right_upper_x - movespeed
	playroom_b_right_lower_x = playroom_b_right_lower_x - movespeed
	playroom_b_bottom_x = playroom_b_bottom_x - movespeed
	playroom_b_top_x = playroom_b_top_x - movespeed
	
	hallwaytwo_b_top_x = hallwaytwo_b_top_x - movespeed
	hallwaytwo_b_bottom_x = hallwaytwo_b_bottom_x - movespeed
	hallwaytwo_b_leftdoor_x = hallwaytwo_b_leftdoor_x - movespeed
	hallwaytwo_b_rightdoor_x = hallwaytwo_b_rightdoor_x - movespeed
	hallwaytwothrone_b_rightwall_x = hallwaytwothrone_b_rightwall_x - movespeed
	throneroom_b_leftdoor_x = throneroom_b_leftdoor_x - movespeed
	throneroom_b_rightdoor_x = throneroom_b_rightdoor_x - movespeed
	throneroom_b_leftwall_x = throneroom_b_leftwall_x - movespeed
	thronehall_b_leftwall_x = thronehall_b_leftwall_x - movespeed
	thronehall_b_rightwall_x = thronehall_b_rightwall_x - movespeed
	galaroom_b_rightwall_x = galaroom_b_rightwall_x - movespeed
	galaroom_b_bottomwall_x = galaroom_b_bottomwall_x - movespeed
	galaroom_b_tdoor_right_x = galaroom_b_tdoor_right_x - movespeed
	galaroom_b_tdoor_left_x = galaroom_b_tdoor_left_x - movespeed
	galaroom_b_sdoor_left_x = galaroom_b_sdoor_left_x - movespeed
	galaroom_b_sdoor_right_x = galaroom_b_sdoor_right_x - movespeed
	galahall_b_top_x = galahall_b_top_x - movespeed
	galahall_b_bottom_x = galahall_b_bottom_x - movespeed
	hallconn_b_bottom_x = hallconn_b_bottom_x - movespeed
	hallconn_b_left_x = hallconn_b_left_x - movespeed
	hallconn_b_righth_x = hallconn_b_righth_x - movespeed
	hallconn_b_lefth_x = hallconn_b_lefth_x - movespeed
	hallconn_b_leftv_x = hallconn_b_leftv_x - movespeed
	treasureroom_b_upright_x = treasureroom_b_upright_x - movespeed
	treasureroom_b_rightw_x = treasureroom_b_rightw_x - movespeed
	treasureroom_b_leftw_x = treasureroom_b_leftw_x - movespeed
	hallwayoneb_b_rwall_x = hallwayoneb_b_rwall_x - movespeed
	hallwayoneb_b_lwall_x = hallwayoneb_b_lwall_x - movespeed
	hallwayone_b_twall_x = hallwayone_b_twall_x - movespeed
	hallwayone_b_bwall_x = hallwayone_b_bwall_x - movespeed
	
	playroom_floor_x = playroom_floor_x - movespeed
	halltwo_floor_x = halltwo_floor_x - movespeed
	throneroom_floor_x = throneroom_floor_x - movespeed
	thronehall_floor_x = thronehall_floor_x - movespeed
	galaroom_floor_x = galaroom_floor_x - movespeed
	hallone_floor_x = hallone_floor_x - movespeed
	halloneb_floor_x = halloneb_floor_x - movespeed
	treasureroom_floor_x = treasureroom_floor_x - movespeed
	treasurehall_floor_x = treasurehall_floor_x - movespeed
	galahall_floor_x = galahall_floor_x - movespeed
	
	hallconnection_x = hallconnection_x - movespeed
	
	if len(aiDwarfCollection) > 0:
		for enemydwarf in aiDwarfCollection:
			enemydwarf.x = enemydwarf.x - movespeed
			enemydwarf.area_xpos = enemydwarf.area_xpos - movespeed
	
	# Move the game objects in the game along with the map
	cCounter = 0
	
	while cCounter < len(gameObjectCollection):
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'BOX_CRATE':
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'DWARF_AXE' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_ROOM' and gameObjectCollection[cCounter][1] == 'DWARF_SHIELD' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'PLAYROOM' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] - movespeed
			
		if gameObjectCollection[cCounter][0] == 'THRONE_HALLWAY' and gameObjectCollection[cCounter][1] == 'HEART_ICON' and gameObjectCollection[cCounter][2] == True:
			gameObjectCollection[cCounter][3] = gameObjectCollection[cCounter][3] - movespeed
			
		cCounter = cCounter + 1
		
	

#######################		END OF GAME ENVIRONMENT MOVEMENT OPERATIONS	############################################

#######################		BOUNDARY DETECTION OPERATIONS	########################################

# Detect if @ edge of bounds
def detectLeftBounds():
	
	if humanDwarf.location == 'PLAYROOM' and playroom_b_left_upper_x > (humanDwarf.x-20) and (playroom_b_left_upper_y+400) > (humanDwarf.y-10):
		return True
	if humanDwarf.location == 'PLAYROOM' and playroom_b_left_lower_x > (humanDwarf.x-20) and (playroom_b_left_lower_y) < (humanDwarf.y-10):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and playroom_b_right_upper_x >= (humanDwarf.x-120) and (playroom_b_right_upper_y+400) > (humanDwarf.y-10):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and playroom_b_right_lower_x >= (humanDwarf.x-122) and (playroom_b_right_lower_y) < (humanDwarf.y+22):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and throneroom_b_leftwall_x >= (humanDwarf.x-70):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and thronehall_b_leftwall_x >= (humanDwarf.x-70):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_sdoor_left_x >= (humanDwarf.x-70) and galaroom_b_sdoor_left_y > (humanDwarf.y-277):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_sdoor_right_x >= (humanDwarf.x-70) and galaroom_b_sdoor_right_y < humanDwarf.y:
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and hallconn_b_left_x >= (humanDwarf.x-70):
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and hallconn_b_lefth_y > (humanDwarf.y-70) and hallconn_b_leftv_x > (humanDwarf.x-70):
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and treasureroom_b_leftw_x > (humanDwarf.x-70):
		return True
	if humanDwarf.location == 'HALLWAY_ONEB' and hallwayoneb_b_lwall_x > (humanDwarf.x-70):
		return True
	else:
		return False

def detectUpperBound():
	if humanDwarf.location == 'PLAYROOM' and playroom_b_top_y > (humanDwarf.y-70):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and hallwaytwo_b_top_y > (humanDwarf.y-70):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and hallwaytwo_b_leftdoor_y > (humanDwarf.y-70) and hallwaytwo_b_leftdoor_x > (humanDwarf.x-160):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and hallwaytwo_b_rightdoor_y > (humanDwarf.y-70) and hallwaytwo_b_rightdoor_x < (humanDwarf.x-15):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and throneroom_b_leftdoor_y > (humanDwarf.y-70) and throneroom_b_leftdoor_x > (humanDwarf.x-160):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and throneroom_b_rightdoor_y > (humanDwarf.y-70) and throneroom_b_rightdoor_x < (humanDwarf.x):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_tdoor_left_y > (humanDwarf.y-70) and galaroom_b_tdoor_left_x > (humanDwarf.x-350):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_tdoor_right_y > (humanDwarf.y-70) and galaroom_b_tdoor_right_x < (humanDwarf.x-15):
		return True
	if humanDwarf.location == 'GALA_HALLWAY' and galahall_b_top_y > (humanDwarf.y-70):
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and (hallconn_b_righth_y+100) > (humanDwarf.y-70) and hallconn_b_righth_x < humanDwarf.x:
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and hallconn_b_lefth_y > (humanDwarf.y-70) and (hallconn_b_lefth_x+350) > humanDwarf.x:
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and treasureroom_b_upright_y > (humanDwarf.y-70) and (treasureroom_b_upright_x) < humanDwarf.x:
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and treasureroom_b_upright_y > (humanDwarf.y-70) and (treasureroom_b_upright_x-250)+150 > (humanDwarf.x):
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and (treasureroom_b_upright_y+450) > (humanDwarf.y-70) and treasureroom_b_upright_x < humanDwarf.x:
		return True
	if humanDwarf.location == 'HALLWAY_ONEB' and hallwayone_b_twall_y > (humanDwarf.y-70):
		return True
	if humanDwarf.location == 'HALLWAY_ONE' and hallwayone_b_twall_y > (humanDwarf.y-70):
		return True
	else:
		return False
		
def detectRightBound():	
	if humanDwarf.location == 'PLAYROOM' and playroom_b_right_upper_x < (humanDwarf.x-10) and (playroom_b_right_upper_y+400) > (humanDwarf.y-10):	
		return True
	if humanDwarf.location == 'PLAYROOM' and playroom_b_right_lower_x < (humanDwarf.x-10) and (playroom_b_right_lower_y) < (humanDwarf.y-10):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and hallwaytwothrone_b_rightwall_x < (humanDwarf.x+40):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and hallwaytwothrone_b_rightwall_x < (humanDwarf.x+40):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and thronehall_b_rightwall_x < (humanDwarf.x+30):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_rightwall_x < (humanDwarf.x+30):
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and hallconn_b_righth_x < (humanDwarf.x+30) and (hallconn_b_righth_y+100) > (humanDwarf.y-50):
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and treasureroom_b_rightw_x < (humanDwarf.x+30):
		return True
	if humanDwarf.location == 'HALLWAY_ONEB' and hallwayoneb_b_rwall_x < (humanDwarf.x+30) and hallwayoneb_b_rwall_y < humanDwarf.y:
		return True
	if humanDwarf.location == 'HALLWAY_ONE' and playroom_b_left_upper_x < (humanDwarf.x+60) and (playroom_b_left_upper_y+400) > humanDwarf.y:
		return True
	if humanDwarf.location == 'HALLWAY_ONE' and playroom_b_left_lower_x < (humanDwarf.x+60) and (playroom_b_left_lower_y) < humanDwarf.y:
		return True
	else:
		return False
		
def detectLowerBound():
	if playroom_b_bottom_y < (humanDwarf.y+30) and humanDwarf.location == 'PLAYROOM':
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and hallwaytwo_b_bottom_y < (humanDwarf.y+30) and hallwaytwo_b_bottom_x > (humanDwarf.x-372):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and hallwaytwo_b_leftdoor_y < (humanDwarf.y+30) and hallwaytwo_b_leftdoor_x > (humanDwarf.x-160):
		return True
	if humanDwarf.location == 'HALLWAY_TWO' and hallwaytwo_b_rightdoor_y < (humanDwarf.y+30) and hallwaytwo_b_rightdoor_x < (humanDwarf.x-5):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and throneroom_b_leftdoor_y < (humanDwarf.y+30) and throneroom_b_leftdoor_x > (humanDwarf.x-160):
		return True
	if humanDwarf.location == 'THRONE_ROOM' and throneroom_b_rightdoor_y < (humanDwarf.y+30) and throneroom_b_rightdoor_x < (humanDwarf.x-5):
		return True
	if humanDwarf.location == 'GALA_ROOM' and galaroom_b_bottomwall_y < (humanDwarf.y+30):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and galaroom_b_tdoor_left_y < (humanDwarf.y+30) and galaroom_b_tdoor_left_x > (humanDwarf.x-370):
		return True
	if humanDwarf.location == 'THRONE_HALLWAY' and galaroom_b_tdoor_right_y < (humanDwarf.y+30) and galaroom_b_tdoor_right_x < (humanDwarf.x-15):
		return True
	if humanDwarf.location == 'GALA_HALLWAY' and galahall_b_bottom_y < (humanDwarf.y+30):
		return True
	if humanDwarf.location == 'TREASURE_HALLWAY' and hallconn_b_bottom_y < (humanDwarf.y+30):
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and (treasureroom_b_upright_y+450) < (humanDwarf.y+30) and treasureroom_b_upright_x < humanDwarf.x:
		return True
	if humanDwarf.location == 'TREASURE_ROOM' and (treasureroom_b_upright_y+450) < (humanDwarf.y+30) and (treasureroom_b_upright_x-250)+150 > humanDwarf.x:
		return True
	if humanDwarf.location == 'HALLWAY_ONEB' and treasureroom_b_upright_y < (humanDwarf.y+30) and treasureroom_b_upright_x < humanDwarf.x:
		return True
	if humanDwarf.location == 'HALLWAY_ONEB' and treasureroom_b_upright_y < (humanDwarf.y+30) and (treasureroom_b_upright_x-250)+150 > humanDwarf.x:
		return True
	if humanDwarf.location == 'HALLWAY_ONE' and hallwayone_b_bwall_y < (humanDwarf.y+30):
		return True
	else:
		return False

#######################		END BOUNDARY DETECTION OPERATIONS	########################################

#######################		COLLISION DETECTION OPERATIONS	########################################

def detectbc1_leftside_col():
	
	global humanDwarf
	
	# A seperate collection for each object in the game
	boxCrateCollection = [ ]
	axeCollection = [ ]
	heartCollection = [ ]
	shieldCollection = [ ]
	
	# Seperate objects out into their seperate collections
	for gameobject in gameObjectCollection:
		if gameobject[1] == 'BOX_CRATE':
			boxCrateCollection.append(gameobject)
		if gameobject[1] == 'DWARF_AXE':
			axeCollection.append(gameobject)
		if gameobject[1] == 'DWARF_SHIELD':
			shieldCollection.append(gameobject)
		if gameobject[1] == 'HEART_ICON':
			heartCollection.append(gameobject)
	
	cCounter = 0
	
	# Check to see if there has been a collision with the box crates
	while cCounter < len(boxCrateCollection):
		if boxCrateCollection[cCounter][0] == humanDwarf.location:
			boxx = boxCrateCollection[cCounter][3]
			boxy = boxCrateCollection[cCounter][4]
			
			if boxx <= (humanDwarf.x+20) and boxx > (humanDwarf.x-78) and(humanDwarf.y+18) >= boxy and humanDwarf.y <= (boxy+115):
				return True # Return True as box-crate perm there
				
		cCounter = cCounter + 1
		
	# Reset counter
	cCounter = 0
	
	# Check to see if there has been collision with any of the axes	
	while cCounter < len(axeCollection):
		if axeCollection[cCounter][0] == humanDwarf.location and axeCollection[cCounter][2] == True:
			axex = axeCollection[cCounter][3]
			axey = axeCollection[cCounter][4]
			
			if axex <= (humanDwarf.x) and axey >= (humanDwarf.y-50) and axey < humanDwarf.y:
				moveFloorRight()
				
				gameObjectCollection[cCounter][2] = False
				axeCollection[cCounter][2] = False
				humanDwarf.hasAxe = True
				
				return False # Return False as object dissapears
				
		cCounter = cCounter + 1
		
	# Reset Counter
	cCounter = 0
	
	while cCounter < len(heartCollection):
		if heartCollection[cCounter][0] == humanDwarf.location and heartCollection[cCounter][2] == True:
			heartx = heartCollection[cCounter][3]
			hearty = heartCollection[cCounter][4]
			
			if humanDwarf.x >= (heartx-10) and humanDwarf.y <= (hearty+30):
				gameObjectCollection[cCounter][2] = False
				heartCollection[cCounter][2] = False
				humanDwarf.energy = humanDwarf.energy + 25
				
				return False 
	
		cCounter = cCounter + 1
			
	return False

# Detect right side of box crate01 collision
def detectbc1_rightside_col():
	global humanDwarf
	
	# A seperate collection for each object in the game
	boxCrateCollection = [ ]
	axeCollection = [ ]
	heartCollection = [ ]
	shieldCollection = [ ]
	
	# Seperate objects out into their seperate collections
	for gameobject in gameObjectCollection:
		if gameobject[1] == 'BOX_CRATE':
			boxCrateCollection.append(gameobject)
		if gameobject[1] == 'DWARF_AXE':
			axeCollection.append(gameobject)
		if gameobject[1] == 'DWARF_SHIELD':
			shieldCollection.append(gameobject)
		if gameobject[1] == 'HEART_ICON':
			heartCollection.append(gameobject)

	# Reset counter
	cCounter = 0

	# Check to see if there has been a collision with any of the box crates
	while cCounter < len(boxCrateCollection):
		if boxCrateCollection[cCounter][0] == humanDwarf.location:
			boxx = boxCrateCollection[cCounter][3]
			boxy = boxCrateCollection[cCounter][4]
			
			if boxx > (humanDwarf.x-122) and boxx < (humanDwarf.x+10) and (humanDwarf.y+18) >= boxy and humanDwarf.y <= (boxy+106):
				return True
				
		cCounter = cCounter + 1
		
	# Reset counter 
	cCounter = 0
	
	# Check to see if there has been any collision with any axe objects
	while cCounter < len(axeCollection):
		if axeCollection[cCounter][0] == humanDwarf.location and axeCollection[cCounter][2] == True:
			axex = axeCollection[cCounter][3]
			axey = axeCollection[cCounter][4]
			
			if axex > (humanDwarf.x-70) and axey < (humanDwarf.y) and axey > (humanDwarf.y-50):
				gameObjectCollection[cCounter][2] = False
				axeCollection[cCounter][2] = False
				humanDwarf.hasAxe = True
				
				return False
				
		cCounter = cCounter + 1
				
	# Reset Counter
	cCounter = 0
	
	# Check to see if any shield objects have been collected	
	while cCounter < len(shieldCollection):
		if shieldCollection[cCounter][0] == humanDwarf.location and shieldCollection[cCounter][2] == True:
			shieldx = shieldCollection[cCounter][3]
			shieldy = shieldCollection[cCounter][4]
			
			if shieldx > (330) and shieldy < humanDwarf.y and shieldy > (humanDwarf.y-50) and humanDwarf.hasAxe == True:
				gameObjectCollection[cCounter][2] = False
				shieldCollection[cCounter][2] = False
				humanDwarf.hasShield = True
				
				return False
				
		cCounter = cCounter + 1

	return False

# Bottom side collision detection function
def detectbc1_bottomside_col():
	global humanDwarf
	
	# A seperate collection for each object in the game
	boxCrateCollection = [ ]
	axeCollection = [ ]
	heartCollection = [ ]
	shieldCollection = [ ]
	
	# Seperate objects out into their seperate collections
	for gameobject in gameObjectCollection:
		if gameobject[1] == 'BOX_CRATE':
			boxCrateCollection.append(gameobject)
		if gameobject[1] == 'DWARF_AXE':
			axeCollection.append(gameobject)
		if gameobject[1] == 'DWARF_SHIELD':
			shieldCollection.append(gameobject)
		if gameobject[1] == 'HEART_ICON':
			heartCollection.append(gameobject)
			
	# Reset counter	
	cCounter = 0
	
	# Check to see if player has collided with any of the box-crates
	while cCounter < len(boxCrateCollection):
		if boxCrateCollection[cCounter][0] == humanDwarf.location:
			boxx = boxCrateCollection[cCounter][3]
			boxy = boxCrateCollection[cCounter][4]
			
			if boxy > (humanDwarf.y-120) and boxy < humanDwarf.y and boxx <= (humanDwarf.x+10) and boxx >= (humanDwarf.x-98):
				return True
				
		cCounter = cCounter + 1
		
	# Reset Counter
	cCounter = 0
	
	# Check to see if player has collided with an axe object 
	while cCounter < len(axeCollection):
		if axeCollection[cCounter][0] == humanDwarf.location and axeCollection[cCounter][2] == True:
			axex = axeCollection[cCounter][3]
			axey = axeCollection[cCounter][4]
			
			if axex < humanDwarf.x and axex > (humanDwarf.x-50) and axey > (humanDwarf.y-50):
				gameObjectCollection[cCounter][2] = False
				axeCollection[cCounter][2] = False
				humanDwarf.hasAxe = True
				
				return False
				
		cCounter = cCounter + 1
		
	# Reset Counter
	cCounter = 0
	
	# Check to see if player has collided with a shield object
	while cCounter < len(shieldCollection):
		if shieldCollection[cCounter][0] == humanDwarf.location and shieldCollection[cCounter][2] == True:
			shieldx = shieldCollection[cCounter][3]
			shieldy = shieldCollection[cCounter][4]
			
			if shieldy > (humanDwarf.y-70) and shieldx > 330:
				gameObjectCollection[cCounter][2] = False
				shieldCollection[cCounter][2] = False
				humanDwarf.hasShield = True
				
				return False
				
		cCounter = cCounter + 1
		
	# Reset Counter
	cCounter = 0
	
	# Check to see if player has collided with a heart object
	while cCounter < len(heartCollection):
		if heartCollection[cCounter][0] == humanDwarf.location and heartCollection[cCounter][2] == True:
			heartx = heartCollection[cCounter][3]
			hearty = heartCollection[cCounter][4]
			
			if humanDwarf.x >= (heartx-10) and humanDwarf.y <= (hearty+30):
				gameObjectCollection[cCounter][2] = False
				heartCollection[cCounter][2] = False
				humanDwarf.energy = humanDwarf.energy + 25
				
				return False 
				
		cCounter = cCounter + 1

	return False


# Top side collision detection function	
def detectbc1_topside_col():
	global humanDwarf
	
	# A seperate collection for each object in the game
	boxCrateCollection = [ ]
	axeCollection = [ ]
	heartCollection = [ ]
	shieldCollection = [ ]
	
	# Seperate objects out into their seperate collections
	for gameobject in gameObjectCollection:
		if gameobject[1] == 'BOX_CRATE':
			boxCrateCollection.append(gameobject)
		if gameobject[1] == 'DWARF_AXE':
			axeCollection.append(gameobject)
		if gameobject[1] == 'DWARF_SHIELD':
			shieldCollection.append(gameobject)
		if gameobject[1] == 'HEART_ICON':
			heartCollection.append(gameobject)
	
	cCounter = 0
	
	# Check to see if player has collided with a box crate object
	while cCounter < len(boxCrateCollection):
		if boxCrateCollection[cCounter][0] == humanDwarf.location:
			boxx = boxCrateCollection[cCounter][3]
			boxy = boxCrateCollection[cCounter][4]
			
			if boxy < (humanDwarf.y+22) and boxy > (humanDwarf.y-98) and boxx < (humanDwarf.x+6) and boxx > (humanDwarf.x-114):
				return True	
				
		cCounter = cCounter + 1
		
	# Reset counter
	cCounter = 0
	
	# Check to see if player has collided with an axe object
	while cCounter < len(axeCollection):
		if axeCollection[cCounter][0] == humanDwarf.location and axeCollection[cCounter][2] == True:
			axex = axeCollection[cCounter][3]
			axey = axeCollection[cCounter][4]
			
			if axey <= (humanDwarf.y) and axex < humanDwarf.x and axex > humanDwarf.x-50:
				gameObjectCollection[cCounter][2] = False
				axeCollection[cCounter][2] = False
				humanDwarf.hasAxe = True
				
				return False
				
		cCounter = cCounter + 1
		
	# Reset Counter
	cCounter = 0
	
	# Check to see if a player has collided with a shield object
	while cCounter < len(shieldCollection):
		if shieldCollection[cCounter][0] == humanDwarf.location and shieldCollection[cCounter][2] == True:
			shieldx = shieldCollection[cCounter][3]
			shieldy = shieldCollection[cCounter][4]
			
			if shieldy <= humanDwarf.y and shieldx <= humanDwarf.x and shieldx >= (humanDwarf.x-50) and humanDwarf.hasAxe == True:
				gameObjectCollection[cCounter][2] = False
				shieldCollection[cCounter][2] = False
				humanDwarf.hasShield = True
				
				return False
				
		cCounter = cCounter + 1
			
	return False
			

#######################		END OF COLLISION DETECTION OPERATIONS	########################################

axe_swing = pygame.mixer.Sound('../sfx/axe_swing.wav')

# DECISION ENGINE FUNCTIONS.....

def getDwarfElNo(NameIn):
	dwarfref = -1 # Not found by default
	counter = 0
	
	for enemydwarf in aiDwarfCollection:
		if enemydwarf.name == NameIn:
			dwarfref = counter
			
		counter = counter + 1
	
	# Return the result
	return dwarfref
	

# A function that triggers enemy chracter movement deponding on room / area enemy character is in
def performEnemyDwarfPatrol():
	# Include y of enemy dwarf
	
	global aiDwarfCollection
	patrolMoveSpeed = 2
	
	# Check to see if there are any enemy dwarfs left 
	dwarfno = len(aiDwarfCollection)
	
	# PLAYROOM Control
	
	if dwarfno > 0:
		
		ronaldDwarf = getDwarfElNo('Ronald')
		donaldDwarf = getDwarfElNo('Donald')
		murphyDwarf = getDwarfElNo('Murphy')
		lewisDwarf = getDwarfElNo('Lewis')
		tomDwarf = getDwarfElNo('Tom')
		jerryDwarf = getDwarfElNo('Jerry')
	
		if ronaldDwarf > -1:		
			if aiDwarfCollection[ronaldDwarf].y < playroom_b_bottom_y and aiDwarfCollection[ronaldDwarf].direction_indicator == DOWN_DIRECTION:
				if aiDwarfCollection[ronaldDwarf].stopMoving == False:
					aiDwarfCollection[ronaldDwarf].processWalk_Anim(DOWN_DIRECTION)
					aiDwarfCollection[ronaldDwarf].y = aiDwarfCollection[ronaldDwarf].y + patrolMoveSpeed
					aiDwarfCollection[ronaldDwarf].area_ypos = aiDwarfCollection[ronaldDwarf].area_ypos + patrolMoveSpeed
		
			if aiDwarfCollection[ronaldDwarf].y >= playroom_b_bottom_y and aiDwarfCollection[ronaldDwarf].direction_indicator == DOWN_DIRECTION:
				aiDwarfCollection[ronaldDwarf].walk_angle = 0
				aiDwarfCollection[ronaldDwarf].walk_target_angle = 0
				aiDwarfCollection[ronaldDwarf].direction_indicator = UP_DIRECTION
		
			if aiDwarfCollection[ronaldDwarf].y > (playroom_b_right_upper_y+60) and aiDwarfCollection[ronaldDwarf].direction_indicator == UP_DIRECTION:
				if aiDwarfCollection[ronaldDwarf].stopMoving == False:
					aiDwarfCollection[ronaldDwarf].processWalk_Anim(UP_DIRECTION)
					aiDwarfCollection[ronaldDwarf].y = aiDwarfCollection[ronaldDwarf].y - patrolMoveSpeed
					aiDwarfCollection[ronaldDwarf].area_ypos = aiDwarfCollection[ronaldDwarf].area_ypos - patrolMoveSpeed
		
			if aiDwarfCollection[ronaldDwarf].y <= (playroom_b_right_upper_y+60) and aiDwarfCollection[ronaldDwarf].direction_indicator == UP_DIRECTION:
				aiDwarfCollection[ronaldDwarf].walk_target_angle = 170
				aiDwarfCollection[ronaldDwarf].walk_angle = 180
				aiDwarfCollection[ronaldDwarf].direction_indicator = DOWN_DIRECTION

			if aiDwarfCollection[ronaldDwarf].stopMoving == True and aiDwarfCollection[ronaldDwarf].attackPossible == True:
				aiDwarfCollection[ronaldDwarf].attack = True				
			else:
				aiDwarfCollection[ronaldDwarf].attack = False
				
		
		# HALLWAY_TWO Control

		if donaldDwarf > -1:
			if aiDwarfCollection[donaldDwarf].stopMoving == False:
				if aiDwarfCollection[donaldDwarf].x < (hallwaytwo_b_rightdoor_x-50) and aiDwarfCollection[donaldDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[donaldDwarf].x = aiDwarfCollection[donaldDwarf].x + patrolMoveSpeed
					aiDwarfCollection[donaldDwarf].area_xpos = aiDwarfCollection[donaldDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[donaldDwarf].processWalk_Anim(RIGHT_DIRECTION)
			
				if aiDwarfCollection[donaldDwarf].x >= (hallwaytwo_b_rightdoor_x-50) and aiDwarfCollection[donaldDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[donaldDwarf].walk_angle = -270
					aiDwarfCollection[donaldDwarf].walk_target_angle = -260
					aiDwarfCollection[donaldDwarf].direction_indicator = LEFT_DIRECTION

				if aiDwarfCollection[donaldDwarf].x > (door_x2_playroom+100) and aiDwarfCollection[donaldDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[donaldDwarf].x = aiDwarfCollection[donaldDwarf].x - patrolMoveSpeed
					aiDwarfCollection[donaldDwarf].area_xpos = aiDwarfCollection[donaldDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[donaldDwarf].processWalk_Anim(LEFT_DIRECTION)
			
				if aiDwarfCollection[donaldDwarf].x <= (door_x2_playroom+100) and aiDwarfCollection[donaldDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[donaldDwarf].walk_angle = -90
					aiDwarfCollection[donaldDwarf].walk_target_angle = -80
					aiDwarfCollection[donaldDwarf].direction_indicator = RIGHT_DIRECTION
					
			if aiDwarfCollection[donaldDwarf].stopMoving == True and aiDwarfCollection[donaldDwarf].attackPossible == True:
				aiDwarfCollection[donaldDwarf].attack = True				
			else:
				aiDwarfCollection[donaldDwarf].attack = False
					
		
		# THRONE ROOM Control
		
		if murphyDwarf > -1:
			if aiDwarfCollection[murphyDwarf].stopMoving == False:
				if aiDwarfCollection[murphyDwarf].x < (hallwaytwothrone_b_rightwall_x-50) and aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[murphyDwarf].x = aiDwarfCollection[murphyDwarf].x + patrolMoveSpeed
					aiDwarfCollection[murphyDwarf].area_xpos = aiDwarfCollection[murphyDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[murphyDwarf].processWalk_Anim(RIGHT_DIRECTION)
					
				if aiDwarfCollection[murphyDwarf].x >= (hallwaytwothrone_b_rightwall_x-50) and aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[murphyDwarf].walk_angle = -270
					aiDwarfCollection[murphyDwarf].walk_target_angle = -260
					aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
					
				if aiDwarfCollection[murphyDwarf].x > (throneroom_b_leftwall_x+50) and aiDwarfCollection[murphyDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].x = aiDwarfCollection[murphyDwarf].x - patrolMoveSpeed
					aiDwarfCollection[murphyDwarf].area_xpos = aiDwarfCollection[murphyDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[murphyDwarf].processWalk_Anim(LEFT_DIRECTION)
					
				if aiDwarfCollection[murphyDwarf].x <= (throneroom_b_leftwall_x+50) and aiDwarfCollection[murphyDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].walk_angle = -90
					aiDwarfCollection[murphyDwarf].walk_target_angle = -80
					aiDwarfCollection[murphyDwarf].direction_indicator = RIGHT_DIRECTION
					
			if aiDwarfCollection[murphyDwarf].stopMoving == True and aiDwarfCollection[murphyDwarf].attackPossible == True:
				aiDwarfCollection[murphyDwarf].attack = True				
			else:
				aiDwarfCollection[murphyDwarf].attack = False
					
		if lewisDwarf > -1:
			if aiDwarfCollection[lewisDwarf].stopMoving == False:
				if aiDwarfCollection[lewisDwarf].x < (hallwaytwothrone_b_rightwall_x-50) and aiDwarfCollection[lewisDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].x = aiDwarfCollection[lewisDwarf].x + patrolMoveSpeed
					aiDwarfCollection[lewisDwarf].area_xpos = aiDwarfCollection[lewisDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[lewisDwarf].processWalk_Anim(RIGHT_DIRECTION)
					
				if aiDwarfCollection[lewisDwarf].x >= (hallwaytwothrone_b_rightwall_x-50) and aiDwarfCollection[lewisDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].walk_angle = -270
					aiDwarfCollection[lewisDwarf].walk_target_angle = -260					
					aiDwarfCollection[lewisDwarf].direction_indicator = LEFT_DIRECTION
					
				if aiDwarfCollection[lewisDwarf].x > (throneroom_b_leftwall_x-50) and aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[lewisDwarf].x = aiDwarfCollection[lewisDwarf].x - patrolMoveSpeed
					aiDwarfCollection[lewisDwarf].area_xpos = aiDwarfCollection[lewisDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[lewisDwarf].processWalk_Anim(LEFT_DIRECTION)
					
				if aiDwarfCollection[lewisDwarf].x <= (throneroom_b_leftwall_x+50) and aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[lewisDwarf].walk_angle = -90
					aiDwarfCollection[lewisDwarf].walk_target_angle = -80					
					aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
					
			if aiDwarfCollection[lewisDwarf].stopMoving == True and aiDwarfCollection[lewisDwarf].attackPossible == True:
				aiDwarfCollection[lewisDwarf].attack = True				
			else:
				aiDwarfCollection[lewisDwarf].attack = False
					
		# GALA ROOM CONTROL
		
		# Set Tom on a horizontal patrol
		if tomDwarf > -1:
			if aiDwarfCollection[tomDwarf].stopMoving == False:
				if aiDwarfCollection[tomDwarf].x < (galaroom_b_rightwall_x-50) and aiDwarfCollection[tomDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[tomDwarf].x = aiDwarfCollection[tomDwarf].x + patrolMoveSpeed
					aiDwarfCollection[tomDwarf].area_xpos = aiDwarfCollection[tomDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[tomDwarf].processWalk_Anim(RIGHT_DIRECTION)
					
				if aiDwarfCollection[tomDwarf].x >= (galaroom_b_rightwall_x-50) and aiDwarfCollection[tomDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[tomDwarf].walk_angle = -270
					aiDwarfCollection[tomDwarf].walk_target_angle = -260					
					aiDwarfCollection[tomDwarf].direction_indicator = LEFT_DIRECTION
					
				if aiDwarfCollection[tomDwarf].x > (galaroom_b_tdoor_left_x-50) and aiDwarfCollection[tomDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[tomDwarf].x = aiDwarfCollection[tomDwarf].x - patrolMoveSpeed
					aiDwarfCollection[tomDwarf].area_xpos = aiDwarfCollection[tomDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[tomDwarf].processWalk_Anim(LEFT_DIRECTION)
					
				if aiDwarfCollection[tomDwarf].x <= (galaroom_b_tdoor_left_x+50) and aiDwarfCollection[tomDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[tomDwarf].walk_angle = -90
					aiDwarfCollection[tomDwarf].walk_target_angle = -80
					aiDwarfCollection[tomDwarf].direction_indicator = RIGHT_DIRECTION
					
			if aiDwarfCollection[tomDwarf].stopMoving == True and aiDwarfCollection[tomDwarf].attackPossible == True:
				aiDwarfCollection[tomDwarf].attack = True				
			else:
				aiDwarfCollection[tomDwarf].attack = False
					
		# Set Jerry on a vertical patrol
		if jerryDwarf > -1:
			if aiDwarfCollection[jerryDwarf].stopMoving == False:
				if aiDwarfCollection[jerryDwarf].y > (galaroom_b_tdoor_left_y-300) and aiDwarfCollection[jerryDwarf].direction_indicator == UP_DIRECTION:
					aiDwarfCollection[jerryDwarf].y = aiDwarfCollection[jerryDwarf].y - patrolMoveSpeed
					aiDwarfCollection[jerryDwarf].area_ypos = aiDwarfCollection[jerryDwarf].area_ypos - patrolMoveSpeed
					aiDwarfCollection[jerryDwarf].processWalk_Anim(UP_DIRECTION)
					
				if aiDwarfCollection[jerryDwarf].y <= (galaroom_b_tdoor_left_y+300) and aiDwarfCollection[jerryDwarf].direction_indicator == UP_DIRECTION:
					aiDwarfCollection[jerryDwarf].walk_angle = 180
					aiDwarfCollection[jerryDwarf].walk_target_angle = 170
					aiDwarfCollection[jerryDwarf].direction_indicator = DOWN_DIRECTION
				
				if aiDwarfCollection[jerryDwarf].y < (galaroom_b_bottomwall_y-50) and aiDwarfCollection[jerryDwarf].direction_indicator == DOWN_DIRECTION:
					aiDwarfCollection[jerryDwarf].y = aiDwarfCollection[jerryDwarf].y + patrolMoveSpeed
					aiDwarfCollection[jerryDwarf].area_ypos = aiDwarfCollection[jerryDwarf].area_ypos + patrolMoveSpeed
					aiDwarfCollection[jerryDwarf].processWalk_Anim(DOWN_DIRECTION)
					
				if aiDwarfCollection[jerryDwarf].y >= (galaroom_b_bottomwall_y-50) and aiDwarfCollection[jerryDwarf].direction_indicator == DOWN_DIRECTION:
					aiDwarfCollection[jerryDwarf].walk_angle = 0
					aiDwarfCollection[jerryDwarf].walk_target_angle = 0
					aiDwarfCollection[jerryDwarf].direction_indicator = UP_DIRECTION
					
			if aiDwarfCollection[jerryDwarf].stopMoving == True and aiDwarfCollection[jerryDwarf].attackPossible == True:
				aiDwarfCollection[jerryDwarf].attack = True				
			else:
				aiDwarfCollection[jerryDwarf].attack = False
					
					
		# TREASURE HALLWAY CONTROL
		tangoDwarf = getDwarfElNo('Tango')
		cashDwarf = getDwarfElNo('Cash')
		
		if tangoDwarf > -1:
			if aiDwarfCollection[tangoDwarf].stopMoving == False:
				if aiDwarfCollection[tangoDwarf].y > (treasureroom_b_upright_y+450)-150 and aiDwarfCollection[tangoDwarf].direction_indicator == UP_DIRECTION:
					aiDwarfCollection[tangoDwarf].y = aiDwarfCollection[tangoDwarf].y - patrolMoveSpeed
					aiDwarfCollection[tangoDwarf].area_ypos = aiDwarfCollection[tangoDwarf].area_ypos - patrolMoveSpeed
					aiDwarfCollection[tangoDwarf].processWalk_Anim(UP_DIRECTION)
					
				if aiDwarfCollection[tangoDwarf].y <= (treasureroom_b_upright_y+450)+150 and aiDwarfCollection[tangoDwarf].direction_indicator == UP_DIRECTION:
					aiDwarfCollection[tangoDwarf].walk_angle = 180
					aiDwarfCollection[tangoDwarf].walk_target_angle = 170
					aiDwarfCollection[tangoDwarf].direction_indicator = DOWN_DIRECTION
					
				if aiDwarfCollection[tangoDwarf].y < (hallconn_b_bottom_y-50) and aiDwarfCollection[tangoDwarf].direction_indicator == DOWN_DIRECTION:
					aiDwarfCollection[tangoDwarf].y = aiDwarfCollection[tangoDwarf].y + patrolMoveSpeed
					aiDwarfCollection[tangoDwarf].area_ypos = aiDwarfCollection[tangoDwarf].area_ypos + patrolMoveSpeed
					aiDwarfCollection[tangoDwarf].processWalk_Anim(DOWN_DIRECTION)
					
				if aiDwarfCollection[tangoDwarf].y >= (hallconn_b_bottom_y-50) and aiDwarfCollection[tangoDwarf].direction_indicator == DOWN_DIRECTION:
					aiDwarfCollection[tangoDwarf].walk_angle = 0
					aiDwarfCollection[tangoDwarf].walk_target_angle = 0
					aiDwarfCollection[tangoDwarf].direction_indicator = UP_DIRECTION
					
			if aiDwarfCollection[tangoDwarf].stopMoving == True and aiDwarfCollection[tangoDwarf].attackPossible == True:
				aiDwarfCollection[tangoDwarf].attack = True				
			else:
				aiDwarfCollection[tangoDwarf].attack = False
					
					
		if cashDwarf > -1:
			if aiDwarfCollection[cashDwarf].stopMoving == False:
				if aiDwarfCollection[cashDwarf].x > (hallconn_b_left_x+100) and aiDwarfCollection[cashDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[cashDwarf].x = aiDwarfCollection[cashDwarf].x - patrolMoveSpeed
					aiDwarfCollection[cashDwarf].area_xpos = aiDwarfCollection[cashDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[cashDwarf].processWalk_Anim(LEFT_DIRECTION)
					
				if aiDwarfCollection[cashDwarf].x <= (hallconn_b_left_x+100) and aiDwarfCollection[cashDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[cashDwarf].walk_angle = -90
					aiDwarfCollection[cashDwarf].walk_target_angle = -80
					aiDwarfCollection[cashDwarf].direction_indicator = RIGHT_DIRECTION

				if aiDwarfCollection[cashDwarf].x < (door_x2_gala-50) and aiDwarfCollection[cashDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[cashDwarf].x = aiDwarfCollection[cashDwarf].x + patrolMoveSpeed
					aiDwarfCollection[cashDwarf].area_xpos = aiDwarfCollection[cashDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[cashDwarf].processWalk_Anim(RIGHT_DIRECTION)
					
				if aiDwarfCollection[cashDwarf].x >= (door_x2_gala-50) and aiDwarfCollection[cashDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[cashDwarf].walk_angle = -270
					aiDwarfCollection[cashDwarf].walk_target_angle = -260
					aiDwarfCollection[cashDwarf].direction_indicator = LEFT_DIRECTION
					
			if aiDwarfCollection[cashDwarf].stopMoving == True and aiDwarfCollection[cashDwarf].attackPossible == True:
				aiDwarfCollection[cashDwarf].attack = True				
			else:
				aiDwarfCollection[cashDwarf].attack = False
					
					
		# HALLWAY ONE CONTROL
		
		geraldDwarf = getDwarfElNo('Gerald')
		
		if geraldDwarf > -1:
			if aiDwarfCollection[geraldDwarf].stopMoving == False:
				if aiDwarfCollection[geraldDwarf].x > (hallwayoneb_b_lwall_x+50) and aiDwarfCollection[geraldDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[geraldDwarf].x = aiDwarfCollection[geraldDwarf].x - patrolMoveSpeed
					aiDwarfCollection[geraldDwarf].area_xpos = aiDwarfCollection[geraldDwarf].area_xpos - patrolMoveSpeed
					aiDwarfCollection[geraldDwarf].processWalk_Anim(LEFT_DIRECTION)
					
				if aiDwarfCollection[geraldDwarf].x <= (hallwayoneb_b_lwall_x+50) and aiDwarfCollection[geraldDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[geraldDwarf].walk_angle = -90
					aiDwarfCollection[geraldDwarf].walk_target_angle = -80
					aiDwarfCollection[geraldDwarf].direction_indicator = RIGHT_DIRECTION
					
				if aiDwarfCollection[geraldDwarf].x < (door_x1_playroom-50) and aiDwarfCollection[geraldDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[geraldDwarf].x = aiDwarfCollection[geraldDwarf].x + patrolMoveSpeed
					aiDwarfCollection[geraldDwarf].area_xpos = aiDwarfCollection[geraldDwarf].area_xpos + patrolMoveSpeed
					aiDwarfCollection[geraldDwarf].processWalk_Anim(RIGHT_DIRECTION)
					
				if aiDwarfCollection[geraldDwarf].x >= (door_x1_playroom-50) and aiDwarfCollection[geraldDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[geraldDwarf].walk_angle = -270
					aiDwarfCollection[geraldDwarf].walk_target_angle = -260
					aiDwarfCollection[geraldDwarf].direction_indicator = LEFT_DIRECTION
					
			if aiDwarfCollection[geraldDwarf].stopMoving == True and aiDwarfCollection[geraldDwarf].attackPossible == True:
				aiDwarfCollection[geraldDwarf].attack = True				
			else:
				aiDwarfCollection[geraldDwarf].attack = False
					
				
# Keep track of human dwarf location 
def updatePlayerLocation():
	global humanDwarf
	
	global door_x2_playroom
	global door_x1_playroom
	global door_y1_throne
	global door_y2_throne
	global door_y1_gala
	global door_x2_gala
	global galahall_floor_x
	global door_y1_treasure
	global door_y2_treasure
	global hallwayoneb_b_rwall_x
	
	# Determine Player Location
	if humanDwarf.location == 'PLAYROOM' and door_x2_playroom < humanDwarf.x:
		humanDwarf.location = 'HALLWAY_TWO'
		
	if humanDwarf.location == 'PLAYROOM' and door_x1_playroom > humanDwarf.x:
		humanDwarf.location = 'HALLWAY_ONE'
		
	if humanDwarf.location == 'HALLWAY_ONE' and door_x1_playroom < humanDwarf.x:
		humanDwarf.location = 'PLAYROOM'
		
	if humanDwarf.location == 'HALLWAY_TWO' and door_x2_playroom > humanDwarf.x:
		humanDwarf.location = 'PLAYROOM'
		
	if humanDwarf.location == 'HALLWAY_TWO' and door_y1_throne < (humanDwarf.y-40):
		humanDwarf.location = 'THRONE_ROOM'
		
	if humanDwarf.location == 'THRONE_ROOM' and door_y1_throne > humanDwarf.y:
		humanDwarf.location = 'HALLWAY_TWO'
		
	if humanDwarf.location == 'THRONE_ROOM' and door_y2_throne < humanDwarf.y:
		humanDwarf.location = 'THRONE_HALLWAY'
		
	if humanDwarf.location == 'THRONE_HALLWAY' and door_y2_throne > humanDwarf.y:
		humanDwarf.location = 'THRONE_ROOM'
		
	if humanDwarf.location == 'THRONE_HALLWAY' and door_y1_gala < (humanDwarf.y-40):
		humanDwarf.location = 'GALA_ROOM'
		
	if humanDwarf.location == 'GALA_ROOM' and door_y1_gala > (humanDwarf.y-40):
		humanDwarf.location = 'THRONE_HALLWAY'
		
	if humanDwarf.location == 'GALA_ROOM' and door_x2_gala > humanDwarf.x:
		humanDwarf.location = 'GALA_HALLWAY'
		
	if humanDwarf.location == 'GALA_HALLWAY' and door_x2_gala < humanDwarf.x:
		humanDwarf.location = 'GALA_ROOM'
		
	if humanDwarf.location == 'GALA_HALLWAY' and galahall_floor_x > humanDwarf.x:
		humanDwarf.location = 'TREASURE_HALLWAY'
		
	if humanDwarf.location == 'TREASURE_HALLWAY' and galahall_floor_x < humanDwarf.x:
		humanDwarf.location = 'GALA_HALLWAY'
		
	if humanDwarf.location == 'TREASURE_HALLWAY' and door_y2_treasure > humanDwarf.y:
		humanDwarf.location = 'TREASURE_ROOM'
		
	if humanDwarf.location == 'TREASURE_ROOM' and door_y2_treasure < (humanDwarf.y-30):
		humanDwarf.location = 'TREASURE_HALLWAY'
		
	if humanDwarf.location == 'TREASURE_ROOM' and door_y1_treasure > humanDwarf.y:
		humanDwarf.location = 'HALLWAY_ONEB'
		
	if humanDwarf.location == 'HALLWAY_ONEB' and door_y1_treasure < humanDwarf.y:
		humanDwarf.location = 'TREASURE_ROOM'
		
	if humanDwarf.location == 'HALLWAY_ONEB' and hallwayoneb_b_rwall_x < humanDwarf.x:
		humanDwarf.location = 'HALLWAY_ONE'
		
	if humanDwarf.location == 'HALLWAY_ONE' and hallwayoneb_b_rwall_x > humanDwarf.x:
		humanDwarf.location = 'HALLWAY_ONEB'

# Called when there has been an attack on the human Dwarf
def reduceHumanDwarfEnergy():
	global humanDwarf
	
	if humanDwarf.hasAxe == True and humanDwarf.hasShield == True:
		humanDwarf.energy = humanDwarf.energy - 2
		
	if humanDwarf.hasAxe == True and humanDwarf.hasShield == False:
		humanDwarf.energy = humanDwarf.energy - 5
		
	if humanDwarf.hasAxe == False and humanDwarf.hasShield == False:
		humanDwarf.energy = humanDwarf.energy - 10


# Process an enemy dwarf attack 
def enemyAttackProcessing():
	global aiDwarfCollection
	global humanDwarf
    
	enemyAttackRatio = 4
	attackDelay = 0.0017
    
	# Enemy Attack Processing
	
	ronaldDwarf = getDwarfElNo('Ronald')
	if ronaldDwarf > -1:
		if aiDwarfCollection[ronaldDwarf].attack == True:
			if aiDwarfCollection[ronaldDwarf].angle_build == 0 and aiDwarfCollection[ronaldDwarf].firstAttackPart == False and aiDwarfCollection[ronaldDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[ronaldDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[ronaldDwarf].noOfAttacks=0						
			aiDwarfCollection[ronaldDwarf].attackMove()
			if aiDwarfCollection[ronaldDwarf].direction_indicator == DOWN_DIRECTION and humanDwarf.direction_indicator == UP_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[ronaldDwarf].direction_indicator == UP_DIRECTION and humanDwarf.direction_indicator == DOWN_DIRECTION:
				sleep(attackDelay)
		
	
	donaldDwarf = getDwarfElNo('Donald')
	if donaldDwarf > -1:
		if aiDwarfCollection[donaldDwarf].attack == True:
			if aiDwarfCollection[donaldDwarf].angle_build == 0 and aiDwarfCollection[donaldDwarf].firstAttackPart == False and aiDwarfCollection[donaldDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[donaldDwarf].noOfAttacks >= enemyAttackRatio:
					aiDwarfCollection[donaldDwarf].noOfAttacks = 0
					reduceHumanDwarfEnergy()			
			aiDwarfCollection[donaldDwarf].attackMove()
			if aiDwarfCollection[donaldDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[donaldDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
	
	murphyDwarf = getDwarfElNo('Murphy')
	if murphyDwarf > -1:
		if aiDwarfCollection[murphyDwarf].attack == True:
			if aiDwarfCollection[murphyDwarf].angle_build == 0 and aiDwarfCollection[murphyDwarf].firstAttackPart == False and aiDwarfCollection[murphyDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[murphyDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[murphyDwarf].noOfAttacks = 0
			aiDwarfCollection[murphyDwarf].attackMove()
			if aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[murphyDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
		
	lewisDwarf = getDwarfElNo('Lewis')
	if lewisDwarf > -1:
		if aiDwarfCollection[lewisDwarf].attack == True:
			if aiDwarfCollection[lewisDwarf].angle_build == 0 and aiDwarfCollection[lewisDwarf].firstAttackPart == False and aiDwarfCollection[lewisDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[lewisDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[lewisDwarf].noOfAttacks = 0
			aiDwarfCollection[lewisDwarf].attackMove()
			if aiDwarfCollection[lewisDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
		
	tomDwarf = getDwarfElNo('Tom')
	if tomDwarf > -1:
		if aiDwarfCollection[tomDwarf].attack == True:
			if aiDwarfCollection[tomDwarf].angle_build == 0 and aiDwarfCollection[tomDwarf].firstAttackPart == False and aiDwarfCollection[tomDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[tomDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[tomDwarf].noOfAttacks = 0
			aiDwarfCollection[tomDwarf].attackMove()
			if aiDwarfCollection[tomDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[tomDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
		
		
	jerryDwarf = getDwarfElNo('Jerry')
	if jerryDwarf > -1:
		if aiDwarfCollection[jerryDwarf].attack == True:
			if aiDwarfCollection[jerryDwarf].angle_build == 0 and aiDwarfCollection[jerryDwarf].firstAttackPart == False and aiDwarfCollection[jerryDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[jerryDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[jerryDwarf].noOfAttacks = 0
			aiDwarfCollection[jerryDwarf].attackMove()
			if aiDwarfCollection[jerryDwarf].direction_indicator == DOWN_DIRECTION and humanDwarf.direction_indicator == UP_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[jerryDwarf].direction_indicator == UP_DIRECTION and humanDwarf.direction_indicator == DOWN_DIRECTION:
				sleep(attackDelay)
		
		
	tangoDwarf = getDwarfElNo('Tango')
	if tangoDwarf > -1:
		if aiDwarfCollection[tangoDwarf].attack == True:
			if aiDwarfCollection[tangoDwarf].angle_build == 0 and aiDwarfCollection[tangoDwarf].firstAttackPart == False and aiDwarfCollection[tangoDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[tangoDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[tangoDwarf].noOfAttacks = 0
			aiDwarfCollection[tangoDwarf].attackMove()
			if aiDwarfCollection[tangoDwarf].direction_indicator == DOWN_DIRECTION and humanDwarf.direction_indicator == UP_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[tangoDwarf].direction_indicator == UP_DIRECTION and humanDwarf.direction_indicator == DOWN_DIRECTION:
				sleep(attackDelay)
		
		
	cashDwarf = getDwarfElNo('Cash')
	if cashDwarf > -1:
		if aiDwarfCollection[cashDwarf].attack == True:
			if aiDwarfCollection[cashDwarf].angle_build == 0 and aiDwarfCollection[cashDwarf].firstAttackPart == False and aiDwarfCollection[cashDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[cashDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[cashDwarf].noOfAttacks = 0
			aiDwarfCollection[cashDwarf].attackMove()
			if aiDwarfCollection[cashDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[cashDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
		
	geraldDwarf = getDwarfElNo('Gerald')
	if geraldDwarf > -1:
		if aiDwarfCollection[geraldDwarf].attack == True:
			if aiDwarfCollection[geraldDwarf].angle_build == 0 and aiDwarfCollection[geraldDwarf].firstAttackPart == False and aiDwarfCollection[geraldDwarf].secondAttackPart == False:
				axe_swing.play()
				if aiDwarfCollection[geraldDwarf].noOfAttacks >= enemyAttackRatio:
					reduceHumanDwarfEnergy()
					aiDwarfCollection[geraldDwarf].noOfAttacks = 0
			aiDwarfCollection[geraldDwarf].attackMove()
			if aiDwarfCollection[geraldDwarf].direction_indicator == RIGHT_DIRECTION and humanDwarf.direction_indicator == LEFT_DIRECTION:
				sleep(attackDelay)
			if aiDwarfCollection[geraldDwarf].direction_indicator == LEFT_DIRECTION and humanDwarf.direction_indicator == RIGHT_DIRECTION:
				sleep(attackDelay)
		
		
	# Enemy Attack Processing End
    
# Process Dwarf AI actions if in attack range
def processInAttackRange():    
	global aiDwarfCollection
	global humanDwarf
    
	if len(aiDwarfCollection) > 0:
		countval = 0
		for enemydwarf in aiDwarfCollection:
			if (enemydwarf.area_xpos+enemydwarf.area_xlength) > (humanDwarf.x) and enemydwarf.area_xpos < humanDwarf.x and enemydwarf.area_ypos < humanDwarf.y and (enemydwarf.area_ypos+enemydwarf.area_ylength) > humanDwarf.y:
				enemydwarf.displayStatus(screen, humanDwarf.x, humanDwarf.y)
				enemydwarf.inRange = True
				aiDwarfCollection[countval].inRange = True
			else:
				aiDwarfCollection[countval].inRange = False
			
			if (enemydwarf.area_xpos+enemydwarf.area_xlength) > (humanDwarf.x) and enemydwarf.area_xpos < humanDwarf.x and enemydwarf.area_ypos < humanDwarf.y and (enemydwarf.area_ypos+enemydwarf.area_ylength) > humanDwarf.y:
				enemydwarf.displayStatus(screen, humanDwarf.x, humanDwarf.y)
				enemydwarf.inRange = True
				aiDwarfCollection[countval].attackPossible = True
				
				if humanDwarf.direction_indicator == UP_DIRECTION and aiDwarfCollection[countval].direction_indicator == DOWN_DIRECTION and aiDwarfCollection[countval].y > (humanDwarf.y-40) and humanDwarf.x <= (aiDwarfCollection[countval].x+20) and humanDwarf.x >= (aiDwarfCollection[countval].x-20):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == DOWN_DIRECTION and aiDwarfCollection[countval].direction_indicator == UP_DIRECTION and aiDwarfCollection[countval].y < (humanDwarf.y+40) and humanDwarf.x <= (aiDwarfCollection[countval].x+20) and humanDwarf.x >= (aiDwarfCollection[countval].x-20):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == LEFT_DIRECTION and (aiDwarfCollection[countval].direction_indicator == UP_DIRECTION or aiDwarfCollection[countval].direction_indicator == DOWN_DIRECTION) and aiDwarfCollection[countval].y > (humanDwarf.y-10) and aiDwarfCollection[countval].y < (humanDwarf.y+10) and aiDwarfCollection[countval].x > (humanDwarf.x-50):
					aiDwarfCollection[countval].stopMoving = True
					aiDwarfCollection[countval].walk_angle = -90
					aiDwarfCollection[countval].walk_target_angle = -80
					aiDwarfCollection[countval].direction_indicator = RIGHT_DIRECTION
					
				if humanDwarf.direction_indicator == RIGHT_DIRECTION and aiDwarfCollection[countval].direction_indicator == LEFT_DIRECTION and aiDwarfCollection[countval].x < (humanDwarf.x+40) and aiDwarfCollection[countval].y >= (humanDwarf.y-20) and aiDwarfCollection[countval].y <= (humanDwarf.y+20):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == LEFT_DIRECTION and aiDwarfCollection[countval].direction_indicator == RIGHT_DIRECTION and aiDwarfCollection[countval].x > (humanDwarf.x-40) and aiDwarfCollection[countval].y >= (humanDwarf.y-20) and aiDwarfCollection[countval].y <= (humanDwarf.y+20):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == DOWN_DIRECTION and aiDwarfCollection[countval].direction_indicator == LEFT_DIRECTION and aiDwarfCollection[countval].x < (humanDwarf.x+40) and aiDwarfCollection[countval].y <= (humanDwarf.y+50):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == UP_DIRECTION and aiDwarfCollection[countval].direction_indicator == LEFT_DIRECTION and aiDwarfCollection[countval].x < (humanDwarf.x+40) and aiDwarfCollection[countval].y >= (humanDwarf.y-20) and aiDwarfCollection[countval].y <= (humanDwarf.y+20):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == DOWN_DIRECTION and aiDwarfCollection[countval].direction_indicator == RIGHT_DIRECTION and aiDwarfCollection[countval].x > (humanDwarf.x-40) and aiDwarfCollection[countval].y <= (humanDwarf.y+50):
					aiDwarfCollection[countval].stopMoving = True
					
				if humanDwarf.direction_indicator == UP_DIRECTION and aiDwarfCollection[countval].direction_indicator == RIGHT_DIRECTION and aiDwarfCollection[countval].x > (humanDwarf.x-40) and aiDwarfCollection[countval].y >= (humanDwarf.y-20) and aiDwarfCollection[countval].y <= (humanDwarf.y+20):
					aiDwarfCollection[countval].stopMoving = True
			else:
				aiDwarfCollection[countval].attackPossible = False
				
			countval = countval + 1

# This function is used to process the result
# of a human dwarf attack            
def processHumanDwarfAttack():
	global aiDwarfCollection
	global humanDwarf
	global axe_swing
	global UP_DIRECTION
	global DOWN_DIRECTION
	global RIGHT_DIRECTION
	global LEFT_DIRECTION
    
	dwarfcount = 0
	if len(aiDwarfCollection) > 0:
		for enemydwarf in aiDwarfCollection:
			if enemydwarf.attackPossible == True and humanDwarf.attack == False:
				aiDwarfCollection[dwarfcount].energy = aiDwarfCollection[dwarfcount].energy - 10
					
				if aiDwarfCollection[dwarfcount].energy <= 0:
					del aiDwarfCollection[dwarfcount]
								
			dwarfcount = dwarfcount + 1
					
	if humanDwarf.attack == False:		
		if humanDwarf.direction_indicator == UP_DIRECTION:
			humanDwarf.walk_angle = 45
			humanDwarf.attack = True
			axe_swing.play()
		if humanDwarf.direction_indicator == RIGHT_DIRECTION:
			humanDwarf.walk_angle = -45
			humanDwarf.attack = True
			axe_swing.play()
		if humanDwarf.direction_indicator == DOWN_DIRECTION:
			humanDwarf.walk_angle = -135
			humanDwarf.attack = True
			axe_swing.play()
		if humanDwarf.direction_indicator == LEFT_DIRECTION:
			humanDwarf.walk_angle = -225
			humanDwarf.attack = True
			axe_swing.play()	
    
# Process enemy action when player moves upwards
# Used when human dwarf is near enemy player
def processEnemyAction_UP_DIRECTION():
	global aiDwarfCollection
	global humanPlayer
    
	if len(aiDwarfCollection) > 0:
			
		# Check to see if Ronald is still alive, if he is then process the following
		ronaldDwarf = getDwarfElNo('Ronald')
			
		if ronaldDwarf > -1:			
			if (aiDwarfCollection[ronaldDwarf].area_ypos+50+aiDwarfCollection[ronaldDwarf].area_ylength/2) > humanDwarf.y and (aiDwarfCollection[ronaldDwarf].area_ypos+50) < (humanDwarf.y-30) and (aiDwarfCollection[ronaldDwarf].area_xpos+50) < humanDwarf.x and (aiDwarfCollection[ronaldDwarf].area_xpos+50+aiDwarfCollection[ronaldDwarf].area_xlength/2) > humanDwarf.x:
				moveFloorUp()
				aiDwarfCollection[ronaldDwarf].stopMoving = True
			else:
				if aiDwarfCollection[ronaldDwarf].attackPossible == False and aiDwarfCollection[0].stopMoving == True:
					aiDwarfCollection[ronaldDwarf].direction_indicator = UP_DIRECTION
					aiDwarfCollection[ronaldDwarf].walk_angle = 0
					aiDwarfCollection[ronaldDwarf].walk_target_angle = 0
					aiDwarfCollection[ronaldDwarf].stopMoving = False
						
		donaldDwarf = getDwarfElNo('Donald')
			
		if donaldDwarf > -1:
			if aiDwarfCollection[donaldDwarf].attackPossible == False and aiDwarfCollection[donaldDwarf].stopMoving == True:
				aiDwarfCollection[donaldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[donaldDwarf].walk_angle = -270
				aiDwarfCollection[donaldDwarf].walk_target_angle = -260
				aiDwarfCollection[donaldDwarf].stopMoving = False
					
		murphyDwarf = getDwarfElNo('Murphy')			
		lewisDwarf = getDwarfElNo('Lewis')
			
		if murphyDwarf > -1 and lewisDwarf > -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				if aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -90
					aiDwarfCollection[murphyDwarf].walk_target_angle = -80
					aiDwarfCollection[murphyDwarf].stopMoving = False
				else:
					aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -270
					aiDwarfCollection[murphyDwarf].walk_target_angle = -260
					aiDwarfCollection[murphyDwarf].stopMoving = False
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[lewisDwarf].stopMoving == True:
				if aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -270
					aiDwarfCollection[lewisDwarf].walk_target_angle = -260
					aiDwarfCollection[lewisDwarf].stopMoving = False
				else:
					aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -90
					aiDwarfCollection[lewisDwarf].walk_target_angle = -80
					aiDwarfCollection[lewisDwarf].stopMoving = False
						
		if murphyDwarf > -1 and lewisDwarf == -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[murphyDwarf].walk_angle = -270
				aiDwarfCollection[murphyDwarf].walk_target_angle = -260
				aiDwarfCollection[murphyDwarf].stopMoving = False
					
		if murphyDwarf == -1 and lewisDwarf > -1:
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[lewisDwarf].walk_angle = -90
				aiDwarfCollection[lewisDwarf].walk_target_angle = -80
				aiDwarfCollection[lewisDwarf].stopMoving = False
					
		tomDwarf = getDwarfElNo('Tom')
		jerryDwarf = getDwarfElNo('Jerry')
			
		if tomDwarf > -1:
			if aiDwarfCollection[tomDwarf].attackPossible == False and aiDwarfCollection[tomDwarf].stopMoving == True:
				aiDwarfCollection[tomDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[tomDwarf].walk_angle = -90
				aiDwarfCollection[tomDwarf].walk_target_angle = -80
				aiDwarfCollection[tomDwarf].stopMoving = False
					
		if jerryDwarf > -1:
			if aiDwarfCollection[jerryDwarf].attackPossible == False and aiDwarfCollection[jerryDwarf].stopMoving == True:
				aiDwarfCollection[jerryDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[jerryDwarf].walk_angle = 0
				aiDwarfCollection[jerryDwarf].walk_target_angle = 0
				aiDwarfCollection[jerryDwarf].stopMoving = False
					
		tangoDwarf = getDwarfElNo('Tango')
		cashDwarf = getDwarfElNo('Cash')
			
		if tangoDwarf > -1:
			if aiDwarfCollection[tangoDwarf].attackPossible == False and aiDwarfCollection[tangoDwarf].stopMoving == True:
				aiDwarfCollection[tangoDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[tangoDwarf].walk_angle = 0
				aiDwarfCollection[tangoDwarf].walk_target_angle = 0
				aiDwarfCollection[tangoDwarf].stopMoving = False
					
		if cashDwarf > -1:
			if aiDwarfCollection[cashDwarf].attackPossible == False and aiDwarfCollection[cashDwarf].stopMoving == True:
				aiDwarfCollection[cashDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[cashDwarf].walk_angle = -90
				aiDwarfCollection[cashDwarf].walk_target_angle = -80
				aiDwarfCollection[cashDwarf].stopMoving = False
					
		geraldDwarf = getDwarfElNo('Gerald')
			
		if geraldDwarf > -1:
			if aiDwarfCollection[geraldDwarf].attackPossible == False and aiDwarfCollection[geraldDwarf].stopMoving == True:
				aiDwarfCollection[geraldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[geraldDwarf].walk_angle = -270
				aiDwarfCollection[geraldDwarf].walk_target_angle = -260
				aiDwarfCollection[geraldDwarf].stopMoving = False    


# Process enemy action if human player moves to the right (Right cursor key)
def processEnemyAction_RIGHT_DIRECTION():
	global aiDwarfCollection
	global humanDwarf

	if len(aiDwarfCollection) > 0:
		
		# Check to see if Ronald is still alive, if he is then do the following....
		ronaldDwarf = getDwarfElNo('Ronald')
			
		if ronaldDwarf > -1:		
			if (aiDwarfCollection[ronaldDwarf].area_xpos+50) < (humanDwarf.x) and (aiDwarfCollection[ronaldDwarf].area_xpos+50) > (humanDwarf.x-20) and (aiDwarfCollection[ronaldDwarf].area_ypos + 50) < humanDwarf.y and (aiDwarfCollection[ronaldDwarf].area_ypos+50+aiDwarfCollection[ronaldDwarf].area_ylength/2) > humanDwarf.y:
				moveFloorRight()
			else:
				if aiDwarfCollection[ronaldDwarf].attackPossible == False and aiDwarfCollection[ronaldDwarf].stopMoving == True:
					aiDwarfCollection[ronaldDwarf].direction_indicator = UP_DIRECTION
					aiDwarfCollection[ronaldDwarf].walk_angle = 0
					aiDwarfCollection[ronaldDwarf].walk_target_angle = 0
					aiDwarfCollection[ronaldDwarf].stopMoving = False
						
		donaldDwarf = getDwarfElNo('Donald')
			
		if donaldDwarf > -1:
			if aiDwarfCollection[donaldDwarf].attackPossible == False and aiDwarfCollection[donaldDwarf].stopMoving == True:
				aiDwarfCollection[donaldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[donaldDwarf].walk_angle = -270
				aiDwarfCollection[donaldDwarf].walk_target_angle = -260
				aiDwarfCollection[donaldDwarf].stopMoving = False
					
		murphyDwarf = getDwarfElNo('Murphy')			
		lewisDwarf = getDwarfElNo('Lewis')
			
		if murphyDwarf > -1 and lewisDwarf > -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				if aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -90
					aiDwarfCollection[murphyDwarf].walk_target_angle = -80
					aiDwarfCollection[murphyDwarf].stopMoving = False
				else:
					aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -270
					aiDwarfCollection[murphyDwarf].walk_target_angle = -260
					aiDwarfCollection[murphyDwarf].stopMoving = False
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[lewisDwarf].stopMoving == True:
				if aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -270
					aiDwarfCollection[lewisDwarf].walk_target_angle = -260
					aiDwarfCollection[lewisDwarf].stopMoving = False
				else:
					aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -90
					aiDwarfCollection[lewisDwarf].walk_target_angle = -80
					aiDwarfCollection[lewisDwarf].stopMoving = False
						
		if murphyDwarf > -1 and lewisDwarf == -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[murphyDwarf].walk_angle = -270
				aiDwarfCollection[murphyDwarf].walk_target_angle = -260
				aiDwarfCollection[murphyDwarf].stopMoving = False
					
		if murphyDwarf == -1 and lewisDwarf > -1:
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[lewisDwarf].walk_angle = -90
				aiDwarfCollection[lewisDwarf].walk_target_angle = -80
				aiDwarfCollection[lewisDwarf].stopMoving = False
					
		tomDwarf = getDwarfElNo('Tom')
		jerryDwarf = getDwarfElNo('Jerry')
			
		if tomDwarf > -1:
			if aiDwarfCollection[tomDwarf].attackPossible == False and aiDwarfCollection[tomDwarf].stopMoving == True:
				aiDwarfCollection[tomDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[tomDwarf].walk_angle = -90
				aiDwarfCollection[tomDwarf].walk_target_angle = -80
				aiDwarfCollection[tomDwarf].stopMoving = False
					
		if jerryDwarf > -1:
			if aiDwarfCollection[jerryDwarf].attackPossible == False and aiDwarfCollection[jerryDwarf].stopMoving == True:
				aiDwarfCollection[jerryDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[jerryDwarf].walk_angle = 0
				aiDwarfCollection[jerryDwarf].walk_target_angle = 0
				aiDwarfCollection[jerryDwarf].stopMoving = False
					
		tangoDwarf = getDwarfElNo('Tango')
		cashDwarf = getDwarfElNo('Cash')
			
		if tangoDwarf > -1:
			if aiDwarfCollection[tangoDwarf].attackPossible == False and aiDwarfCollection[tangoDwarf].stopMoving == True:
				aiDwarfCollection[tangoDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[tangoDwarf].walk_angle = 0
				aiDwarfCollection[tangoDwarf].walk_target_angle = 0
				aiDwarfCollection[tangoDwarf].stopMoving = False
					
		if cashDwarf > -1:
			if aiDwarfCollection[cashDwarf].attackPossible == False and aiDwarfCollection[cashDwarf].stopMoving == True:
				aiDwarfCollection[cashDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[cashDwarf].walk_angle = -90
				aiDwarfCollection[cashDwarf].walk_target_angle = -80
				aiDwarfCollection[cashDwarf].stopMoving = False
			
		geraldDwarf = getDwarfElNo('Gerald')
			
		if geraldDwarf > -1:
			if aiDwarfCollection[geraldDwarf].attackPossible == False and aiDwarfCollection[geraldDwarf].stopMoving == True:
				aiDwarfCollection[geraldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[geraldDwarf].walk_angle = -270
				aiDwarfCollection[geraldDwarf].walk_target_angle = -260
				aiDwarfCollection[geraldDwarf].stopMoving = False

def processEnemyAction_DOWN_DIRECTION():
	global aiDwarfCollection
	global humanDwarf

	if len(aiDwarfCollection) > 0:
		
		# Check to see if Ronald is still alive....
			
		ronaldDwarf = getDwarfElNo('Ronald')
			
		if ronaldDwarf > -1:		
			if (aiDwarfCollection[ronaldDwarf].area_ypos+50) < (humanDwarf.y) and (aiDwarfCollection[ronaldDwarf].area_ypos+50+aiDwarfCollection[ronaldDwarf].area_ylength/2) > (humanDwarf.y+30) and (aiDwarfCollection[ronaldDwarf].area_xpos+50) < humanDwarf.x and (aiDwarfCollection[ronaldDwarf].area_xpos+50+aiDwarfCollection[ronaldDwarf].area_xlength/2) > humanDwarf.x:
				moveFloorDown()
				aiDwarfCollection[ronaldDwarf].stopMoving = True
			else:
				if aiDwarfCollection[ronaldDwarf].attackPossible == False and aiDwarfCollection[ronaldDwarf].stopMoving == True:
					aiDwarfCollection[ronaldDwarf].direction_indicator = UP_DIRECTION
					aiDwarfCollection[ronaldDwarf].walk_angle = 0
					aiDwarfCollection[ronaldDwarf].walk_target_angle = 0
					aiDwarfCollection[ronaldDwarf].stopMoving = False
						
		murphyDwarf = getDwarfElNo('Murphy')			
		lewisDwarf = getDwarfElNo('Lewis')
			
		if murphyDwarf > -1 and lewisDwarf > -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				if aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -90
					aiDwarfCollection[murphyDwarf].walk_target_angle = -80
					aiDwarfCollection[murphyDwarf].stopMoving = False
				else:
					aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -270
					aiDwarfCollection[murphyDwarf].walk_target_angle = -260
					aiDwarfCollection[murphyDwarf].stopMoving = False
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[lewisDwarf].stopMoving == True:
				if aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -270
					aiDwarfCollection[lewisDwarf].walk_target_angle = -260
					aiDwarfCollection[lewisDwarf].stopMoving = False
				else:
					aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -90
					aiDwarfCollection[lewisDwarf].walk_target_angle = -80
					aiDwarfCollection[lewisDwarf].stopMoving = False
						
		if murphyDwarf > -1 and lewisDwarf == -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[murphyDwarf].walk_angle = -270
				aiDwarfCollection[murphyDwarf].walk_target_angle = -260
				aiDwarfCollection[murphyDwarf].stopMoving = False
					
		if murphyDwarf == -1 and lewisDwarf > -1:
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[lewisDwarf].walk_angle = -90
				aiDwarfCollection[lewisDwarf].walk_target_angle = -80
				aiDwarfCollection[lewisDwarf].stopMoving = False
					
		tomDwarf = getDwarfElNo('Tom')
		jerryDwarf = getDwarfElNo('Jerry')
			
		if tomDwarf > -1:
			if aiDwarfCollection[tomDwarf].attackPossible == False and aiDwarfCollection[tomDwarf].stopMoving == True:
				aiDwarfCollection[tomDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[tomDwarf].walk_angle = -90
				aiDwarfCollection[tomDwarf].walk_target_angle = -80
				aiDwarfCollection[tomDwarf].stopMoving = False
					
		if jerryDwarf > -1:
			if aiDwarfCollection[jerryDwarf].attackPossible == False and aiDwarfCollection[jerryDwarf].stopMoving == True:
				aiDwarfCollection[jerryDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[jerryDwarf].walk_angle = 0
				aiDwarfCollection[jerryDwarf].walk_target_angle = 0
				aiDwarfCollection[jerryDwarf].stopMoving = False
					
		tangoDwarf = getDwarfElNo('Tango')
		cashDwarf = getDwarfElNo('Cash')
			
		if tangoDwarf > -1:
			if aiDwarfCollection[tangoDwarf].attackPossible == False and aiDwarfCollection[tangoDwarf].stopMoving == True:
				aiDwarfCollection[tangoDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[tangoDwarf].walk_angle = 0
				aiDwarfCollection[tangoDwarf].walk_target_angle = 0
				aiDwarfCollection[tangoDwarf].stopMoving = False
					
		if cashDwarf > -1:
			if aiDwarfCollection[cashDwarf].attackPossible == False and aiDwarfCollection[cashDwarf].stopMoving == True:
				aiDwarfCollection[cashDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[cashDwarf].walk_angle = -90
				aiDwarfCollection[cashDwarf].walk_target_angle = -80
				aiDwarfCollection[cashDwarf].stopMoving = False
					
		geraldDwarf = getDwarfElNo('Gerald')
			
		if geraldDwarf > -1:
			if aiDwarfCollection[geraldDwarf].attackPossible == False and aiDwarfCollection[geraldDwarf].stopMoving == True:
				aiDwarfCollection[geraldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[geraldDwarf].walk_angle = -270
				aiDwarfCollection[geraldDwarf].walk_target_angle = -260
				aiDwarfCollection[geraldDwarf].stopMoving = False


def processEnemyAction_LEFT_DIRECTION():
	global aiDwarfCollection
	global humanDwarf
    
	if len(aiDwarfCollection) > 0:
			
		ronaldDwarf = getDwarfElNo('Ronald')
			
		if ronaldDwarf > -1:			
			if (aiDwarfCollection[ronaldDwarf].area_xpos+50+aiDwarfCollection[ronaldDwarf].area_xlength/2) > (humanDwarf.x) and (aiDwarfCollection[ronaldDwarf].area_xpos+50) < (humanDwarf.x-20) and (aiDwarfCollection[ronaldDwarf].area_ypos + 50) < humanDwarf.y and (aiDwarfCollection[ronaldDwarf].area_ypos+50+aiDwarfCollection[ronaldDwarf].area_ylength/2) > humanDwarf.y:
				moveFloorLeft()
					
		donaldDwarf = getDwarfElNo('Donald')
			
		if donaldDwarf > -1:
			if aiDwarfCollection[donaldDwarf].attackPossible == False and aiDwarfCollection[donaldDwarf].stopMoving == True:
				aiDwarfCollection[donaldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[donaldDwarf].walk_angle = -270
				aiDwarfCollection[donaldDwarf].walk_target_angle = -260
				aiDwarfCollection[donaldDwarf].stopMoving = False
					
		murphyDwarf = getDwarfElNo('Murphy')			
		lewisDwarf = getDwarfElNo('Lewis')
			
		if murphyDwarf > -1 and lewisDwarf > -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				if aiDwarfCollection[lewisDwarf].direction_indicator == LEFT_DIRECTION:
					aiDwarfCollection[murphyDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -90
					aiDwarfCollection[murphyDwarf].walk_target_angle = -80
					aiDwarfCollection[murphyDwarf].stopMoving = False
				else:
					aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[murphyDwarf].walk_angle = -270
					aiDwarfCollection[murphyDwarf].walk_target_angle = -260
					aiDwarfCollection[murphyDwarf].stopMoving = False
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[lewisDwarf].stopMoving == True:
				if aiDwarfCollection[murphyDwarf].direction_indicator == RIGHT_DIRECTION:
					aiDwarfCollection[lewisDwarf].direction_indicator = LEFT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -270
					aiDwarfCollection[lewisDwarf].walk_target_angle = -260
					aiDwarfCollection[lewisDwarf].stopMoving = False
				else:
					aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
					aiDwarfCollection[lewisDwarf].walk_angle = -90
					aiDwarfCollection[lewisDwarf].walk_target_angle = -80
					aiDwarfCollection[lewisDwarf].stopMoving = False
						
		if murphyDwarf > -1 and lewisDwarf == -1:
			if aiDwarfCollection[murphyDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[murphyDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[murphyDwarf].walk_angle = -270
				aiDwarfCollection[murphyDwarf].walk_target_angle = -260
				aiDwarfCollection[murphyDwarf].stopMoving = False
					
		if murphyDwarf == -1 and lewisDwarf > -1:
			if aiDwarfCollection[lewisDwarf].attackPossible == False and aiDwarfCollection[murphyDwarf].stopMoving == True:
				aiDwarfCollection[lewisDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[lewisDwarf].walk_angle = -90
				aiDwarfCollection[lewisDwarf].walk_target_angle = -80
				aiDwarfCollection[lewisDwarf].stopMoving = False
					
		tomDwarf = getDwarfElNo('Tom')
		jerryDwarf = getDwarfElNo('Jerry')
			
		if tomDwarf > -1:
			if aiDwarfCollection[tomDwarf].attackPossible == False and aiDwarfCollection[tomDwarf].stopMoving == True:
				aiDwarfCollection[tomDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[tomDwarf].walk_angle = -90
				aiDwarfCollection[tomDwarf].walk_target_angle = -80
				aiDwarfCollection[tomDwarf].stopMoving = False
					
		if jerryDwarf > -1:
			if aiDwarfCollection[jerryDwarf].attackPossible == False and aiDwarfCollection[jerryDwarf].stopMoving == True:
				aiDwarfCollection[jerryDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[jerryDwarf].walk_angle = 0
				aiDwarfCollection[jerryDwarf].walk_target_angle = 0
				aiDwarfCollection[jerryDwarf].stopMoving = False
					
		tangoDwarf = getDwarfElNo('Tango')
		cashDwarf = getDwarfElNo('Cash')
			
		if tangoDwarf > -1:
			if aiDwarfCollection[tangoDwarf].attackPossible == False and aiDwarfCollection[tangoDwarf].stopMoving == True:
				aiDwarfCollection[tangoDwarf].direction_indicator = UP_DIRECTION
				aiDwarfCollection[tangoDwarf].walk_angle = 0
				aiDwarfCollection[tangoDwarf].walk_target_angle = 0
				aiDwarfCollection[tangoDwarf].stopMoving = False
					
		if cashDwarf > -1:
			if aiDwarfCollection[cashDwarf].attackPossible == False and aiDwarfCollection[cashDwarf].stopMoving == True:
				aiDwarfCollection[cashDwarf].direction_indicator = RIGHT_DIRECTION
				aiDwarfCollection[cashDwarf].walk_angle = -90
				aiDwarfCollection[cashDwarf].walk_target_angle = -80
				aiDwarfCollection[cashDwarf].stopMoving = False
					
		geraldDwarf = getDwarfElNo('Gerald')
			
		if geraldDwarf > -1:
			if aiDwarfCollection[geraldDwarf].attackPossible == False and aiDwarfCollection[geraldDwarf].stopMoving == True:
				aiDwarfCollection[geraldDwarf].direction_indicator = LEFT_DIRECTION
				aiDwarfCollection[geraldDwarf].walk_angle = -270
				aiDwarfCollection[geraldDwarf].walk_target_angle = -260
				aiDwarfCollection[geraldDwarf].stopMoving = False    

# Render the objects in the game
def renderGameObjects(screenIn):
	global screen
	global gameObjectCollection
	global boxCrate
	global axeimage
	global heart_icon
	global shieldimage
    
	oCounter = 0
	
	while oCounter < len(gameObjectCollection):
		if gameObjectCollection[oCounter][0] == 'PLAYROOM' and gameObjectCollection[oCounter][1] == 'BOX_CRATE':
			screenIn.blit(boxCrate, (int(gameObjectCollection[oCounter][3]), int(gameObjectCollection[oCounter][4])))
			
		if gameObjectCollection[oCounter][0] == 'PLAYROOM' and gameObjectCollection[oCounter][1] == 'DWARF_AXE' and gameObjectCollection[oCounter][2] == True:
			screenIn.blit(axeimage, (int(gameObjectCollection[oCounter][3]), int(gameObjectCollection[oCounter][4])))
			
		if gameObjectCollection[oCounter][0] == 'PLAYROOM' and gameObjectCollection[oCounter][1] == 'HEART_ICON' and gameObjectCollection[oCounter][2] == True:
			screenIn.blit(heart_icon, (int(gameObjectCollection[oCounter][3]), int(gameObjectCollection[oCounter][4])))
			
		if gameObjectCollection[oCounter][0] == 'THRONE_HALLWAY' and gameObjectCollection[oCounter][1] == 'HEART_ICON' and gameObjectCollection[oCounter][2] == True:
			screenIn.blit(heart_icon, (int(gameObjectCollection[oCounter][3]), int(gameObjectCollection[oCounter][4])))
			
		if gameObjectCollection[oCounter][0] == 'THRONE_ROOM' and gameObjectCollection[oCounter][1] == 'DWARF_SHIELD' and gameObjectCollection[oCounter][2] == True:
			screenIn.blit(shieldimage, (int(gameObjectCollection[oCounter][3]), int(gameObjectCollection[oCounter][4])))
			
		oCounter = oCounter + 1    

# Process Human Dwarf Attack Animation
def processHumanAttackAnimation():
	global humanDwarf

	# Process attack animation if needed
	if humanDwarf.attack == True:
		if humanDwarf.direction_indicator == UP_DIRECTION:
			humanDwarf.performAttack_Move(UP_DIRECTION)
		if humanDwarf.direction_indicator == RIGHT_DIRECTION:
			humanDwarf.performAttack_Move(RIGHT_DIRECTION)
		if humanDwarf.direction_indicator == DOWN_DIRECTION:
			humanDwarf.performAttack_Move(DOWN_DIRECTION)			
		if humanDwarf.direction_indicator == LEFT_DIRECTION:
			humanDwarf.performAttack_Move(LEFT_DIRECTION)	    

#################################
##							   ## 
##		PROGRAM ENTRY		   ##
##							   ##
#################################

while not programEnd:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			programEnd = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			programEnd = True
		if event.type == MOUSEBUTTONDOWN:
			mpos = pygame.mouse.get_pos()
			xval = mpos[0]
			yval = mpos[1]
			
	# Update the location of the human player
	updatePlayerLocation()	
	
	# Process enemy attack if needed 
	enemyAttackProcessing()
 
	# Get key input pressed by player
	keys_pressed = pygame.key.get_pressed()

	#########     SPACE KEY PRESSED      ##############
	
	if keys_pressed[pygame.K_SPACE]:		
		processHumanDwarfAttack()
    
    ###################################################
	
	############      UP KEY PRESSED      #############
    
	# Check to see if only the UP key is pressed
	if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_RIGHT] == False and keys_pressed[pygame.K_LEFT] == False:		
		humanDwarf.processWalk_Anim(UP_DIRECTION)
		processEnemyAction_UP_DIRECTION()

		# Detect for possible collision	(boundary or object)	
		if detectUpperBound() == False and detectbc1_bottomside_col() == False:
			moveFloorDown()

    ###################################################
		
	#############   RIGHT CURSOR KEY PRESSED      ############################
    
    # Check to see if only the RIGHT key is pressed
	if keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_UP] == False and keys_pressed[pygame.K_DOWN] == False:
		humanDwarf.processWalk_Anim(RIGHT_DIRECTION)
		processEnemyAction_RIGHT_DIRECTION()
		
		# Detect for possible collision
		if detectRightBound() == False and detectbc1_leftside_col() == False:
			moveFloorLeft()		

    ##########################################################################
	
    #########################       DOWN KEY PRESSED     ##################################################################
    
	# Check to see if down key has only been pressed
	if keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_RIGHT] == False and keys_pressed[pygame.K_LEFT] == False:
		# Process walk animation
		humanDwarf.processWalk_Anim(DOWN_DIRECTION)
		processEnemyAction_DOWN_DIRECTION()

		# Detect for possible collision 
		if detectLowerBound() == False and detectbc1_topside_col() == False:
			moveFloorUp()
	
    #######################################################################################################################
	
    #######################        LEFT KEY PRESSED      #############################################
    
	# Check to see if LEFT key has been pressed
	if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_UP] == False and keys_pressed[pygame.K_DOWN] == False:
		humanDwarf.processWalk_Anim(LEFT_DIRECTION)
		processEnemyAction_LEFT_DIRECTION()
		
		# Detect for possible collision
		if detectLeftBounds() == False and detectbc1_rightside_col() == False:
			moveFloorRight()
			
	###################################################################################################

	# Process Human Dwarf Attack animation
	processHumanAttackAnimation()
	
	# Output background image
	screen.blit(background_image, (0, 0))	

	# Render parts of the game depending on which area the human dwarf is in
	renderGameAreas_OnCondition(humanDwarf.location)
	
	# Render the objects in the game
	renderGameObjects(screen)

	##################################    RENDER HUMAN DWARF    ############################################################### 
	
	if humanDwarf.hasAxe == True:	
		rotated_image = pygame.transform.rotate(playerImageFront01, humanDwarf.walk_angle)		
	if humanDwarf.hasAxe == False and humanDwarf.hasShield == False:
		rotated_image = pygame.transform.rotate(empty_dwarf, humanDwarf.walk_angle)
	if humanDwarf.hasAxe == True and humanDwarf.hasShield == True:
		rotated_image = pygame.transform.rotate(fullarmeddwarf, humanDwarf.walk_angle)
	
	newplayerpos = (round(humanDwarf.x - rotated_image.get_rect().width / 2), round(humanDwarf.y - rotated_image.get_rect().height / 2))
	screen.blit(rotated_image, newplayerpos)

    ###########################################################################################################################
	
    ##################################    RENDER ENEMY DWARF     ##############################################################
    
	# Render Enemy Dwarf player
	if len(aiDwarfCollection) > 0:
		for enemydwarf in aiDwarfCollection:
			rotated_enemy_image = pygame.transform.rotate(enemyDwarf01, enemydwarf.walk_angle)
			newenemypos = (round(enemydwarf.x - rotated_enemy_image.get_rect().width / 2),round(enemydwarf.y - rotated_enemy_image.get_rect().height / 2))
			screen.blit(rotated_enemy_image, newenemypos)
	
    ###########################################################################################################################
    
    #############################     RENDER OUTSIDE BRICKS FOR THE BUILDING      ###############################################
    
	# Only show play room doors if the Playroom is active 
	if showPlayroom == True:	
		# Playroom Walls
		# Vertical Bricks
	
		screen.blit(outsideBrickVert1, (playroom_b_left_upper_x-50,playroom_b_left_upper_y-7))
		screen.blit(outsideBrickVert1, (playroom_b_left_lower_x-50,playroom_b_left_lower_y))	
	
		screen.blit(outsideBrickVert1, (playroom_b_right_upper_x+50,playroom_b_right_upper_y-7))
		screen.blit(outsideBrickVert1, (playroom_b_right_lower_x+50,playroom_b_right_lower_y))
	
		# Horizontal Bricks	
	
		screen.blit(outsideBrickHoriz1, (playroom_b_bottom_x-50, playroom_b_bottom_y))	
		screen.blit(outsideBrickHoriz1, (playroom_b_top_x-50, playroom_b_top_y))		
		
		# Left door on home / base room
		screen.blit(vertDoor, (door_x1_playroom,door_y1_playroom))
	
		# Right door on home / base room
		screen.blit(vertDoor, (door_x2_playroom,door_y2_playroom))	
		
	if showHallWayTwo == True:
		# Hall Two Bricks
		#######	  HALLWAY_TWO Bricks   ####################	
	
		screen.blit(outsideBrickHoriz1, (hallwaytwo_b_top_x, hallwaytwo_b_top_y))	
		screen.blit(outsideBrickHoriz7, (hallwaytwo_b_bottom_x, hallwaytwo_b_bottom_y))	
	
		screen.blit(outsideBrickHoriz3, (hallwaytwo_b_leftdoor_x, hallwaytwo_b_leftdoor_y))	
		screen.blit(outsideBrickHoriz3, (hallwaytwo_b_rightdoor_x, hallwaytwo_b_rightdoor_y))	
	
		screen.blit(outsideBrickVert21, (hallwaytwothrone_b_rightwall_x, hallwaytwothrone_b_rightwall_y))	
	
		###################################################
	
	if showTreasureRoom == True:	
		# Treasure Room Bricks		
		
		# Bricks on right side of door (top)
		screen.blit(outsideBrickHoriz3, (treasureroom_b_upright_x, treasureroom_b_upright_y))
		
		# Bricks on left side of door (top)
		screen.blit(outsideBrickHoriz3, (treasureroom_b_upright_x-250, treasureroom_b_upright_y))
		
		# (Bottom)
		# Left side of door
		screen.blit(outsideBrickHoriz3, (treasureroom_b_upright_x-250, treasureroom_b_upright_y+450))
		
		# Right side of door
		screen.blit(outsideBrickHoriz3, (treasureroom_b_upright_x, treasureroom_b_upright_y+450))		
		
		# Right side wall
		screen.blit(outsideBrickVert8, (treasureroom_b_rightw_x, treasureroom_b_rightw_y))		
		
		# Left side wall
		screen.blit(outsideBrickVert8, (treasureroom_b_leftw_x, treasureroom_b_leftw_y))
		
		# Horizontal door on treasure room
		screen.blit(horizDoor, (door_x1_treasure,door_y1_treasure))	
	
		# Horizontal door on treasure room (exit door)
		screen.blit(horizDoor, (door_x2_treasure, door_y2_treasure))
		
	if showTreasureHall == True:
		screen.blit(outsideBrickHoriz1, (hallconn_b_bottom_x, hallconn_b_bottom_y))
		screen.blit(outsideBrickVert16, (hallconn_b_left_x, hallconn_b_left_y))
		screen.blit(outsideBrickHoriz5, (hallconn_b_righth_x, hallconn_b_righth_y))
		screen.blit(outsideBrickHoriz5, (hallconn_b_righth_x, hallconn_b_righth_y+50))
		screen.blit(outsideBrickHoriz5, (hallconn_b_righth_x, hallconn_b_righth_y+100))
		screen.blit(outsideBrickVert3, (hallconn_b_righth_x, hallconn_b_righth_y-150))
		screen.blit(outsideBrickVert16, (hallconn_b_righth_x, hallconn_b_righth_y-950))		
		
		screen.blit(outsideBrickHoriz7a, (hallconn_b_lefth_x, hallconn_b_lefth_y))
		screen.blit(outsideBrickVert1, (hallconn_b_leftv_x, hallconn_b_leftv_y))
		screen.blit(outsideBrickVert3, (hallconn_b_leftv_x, hallconn_b_leftv_y-100))
		
	if showThroneHall == True:
		# Throne Hall Way Bricks
		###########	  THRONE_HALLWAY Bricks	  #####################
	
		screen.blit(outsideBrickVert21, (thronehall_b_leftwall_x, thronehall_b_leftwall_y-5))
		screen.blit(outsideBrickVert21, (thronehall_b_rightwall_x, thronehall_b_rightwall_y-5))
	
		###########################################################
	
	if showThroneRoom == True:	
		# Throne Room Bricks
		##########	THRONE_ROOM Bricks	###################
	
		screen.blit(outsideBrickHoriz3, (throneroom_b_leftdoor_x, throneroom_b_leftdoor_y))
		screen.blit(outsideBrickHoriz3, (throneroom_b_rightdoor_x, throneroom_b_rightdoor_y))	
	
		screen.blit(outsideBrickVert15, (throneroom_b_leftwall_x, throneroom_b_leftwall_y))
		screen.blit(outsideBrickVert21, (hallwaytwothrone_b_rightwall_x, hallwaytwothrone_b_rightwall_y))
		
	
		####################################################
		
		# Horizontal door on throne room
		screen.blit(horizDoor, (door_x1_throne, door_y1_throne))
	
		# 2nd horizontal door on throne room
		screen.blit(horizDoor, (door_x2_throne, door_y2_throne))
	
	if showGalaRoom == True:	
		# Gala Room Bricks
		###############	  GALA ROOM Bricks	 ######################	
	
		screen.blit(outsideBrickVert16, (galaroom_b_rightwall_x, galaroom_b_rightwall_y))	
		screen.blit(outsideBrickHoriz1, (galaroom_b_bottomwall_x, galaroom_b_bottomwall_y))
	
		screen.blit(outsideBrickHoriz7, (galaroom_b_tdoor_right_x, galaroom_b_tdoor_right_y))
		screen.blit(outsideBrickHoriz7a, (galaroom_b_tdoor_left_x, galaroom_b_tdoor_left_y))	
	
		screen.blit(outsideBrickVert5, (galaroom_b_sdoor_left_x, galaroom_b_sdoor_left_y))
	
		screen.blit(outsideBrickVert8, (galaroom_b_sdoor_right_x, galaroom_b_sdoor_right_y))
		
		##########################################################
		
		# 1st Horizontal door on gala room
		screen.blit(horizDoor, (door_x1_gala, door_y1_gala))
	
		# 2nd vertical door on gala room
		screen.blit(vertDoor, (door_x2_gala, door_y2_gala))
		
	if showGalaHall == True:		
		screen.blit(outsideBrickHoriz30, (galahall_b_top_x, galahall_b_top_y))
		screen.blit(outsideBrickHoriz30, (galahall_b_bottom_x, galahall_b_bottom_y))
		
	if showHallWayOneB == True:
		screen.blit(outsideBrickVert1, (hallwayoneb_b_rwall_x, hallwayoneb_b_rwall_y))
		screen.blit(outsideBrickVert3, (hallwayoneb_b_rwall_x, hallwayoneb_b_rwall_y+350))
		screen.blit(outsideBrickVert15, (hallwayoneb_b_lwall_x, hallwayoneb_b_lwall_y))
	
	if showHallwayOne == True:
		screen.blit(outsideBrickHoriz20, (hallwayone_b_twall_x, hallwayone_b_twall_y))
		screen.blit(outsideBrickHoriz1, (hallwayone_b_bwall_x, hallwayone_b_bwall_y))
	
    ###########################################################################################################
    
	# Display Player status
	humanDwarf.displayStatus(screen)
	
	# Process enemy response if in attack range
	processInAttackRange()
			
	# Only perform enemy dwarf patrol if there enemies left to patrol
	performEnemyDwarfPatrol()

    ############################        GAME END DECISION       ##############################
		
	# Check to see if player has lost
	if humanDwarf.energy <= 0: # Human Player Lost
		screen.blit(gameover_loose, (int(HORIZ_RESOLUTION / 2 / 2), int(VERT_RESOLUTION / 2 / 2)))
		programEnd = True
			
	# Check to see if player has won		
	if len(aiDwarfCollection) == 0: # Human Player Won
		screen.blit(gameover_win, (int(HORIZ_RESOLUTION / 2 / 2), int(VERT_RESOLUTION / 2 / 2)))
		programEnd = True
		
	###########################################################################################
    
	clock.tick(100)	
	pygame.display.flip()

print("End of Program")
sleep(3)
pygame.quit()

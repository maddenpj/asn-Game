#!/usr/bin/python

import pygame 
import os, sys
from random import randrange
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((1024,768))
pygame.display.set_caption('player Python Snakes')
screen = pygame.display.get_surface()
pygame.key.set_repeat(1,50)

playersurface = pygame.image.load('art/player.png').convert()
spawnersurface = pygame.image.load('art/beef_spawner.png').convert()
pythonsurface = pygame.image.load('art/pythons.png').convert()

lastFrame = 0

NEXT_ID = 0

def newID():
	global NEXT_ID
	tmp = NEXT_ID
	NEXT_ID += 1
	return tmp

class GameObject:
	def __init__(self, image, speed):
		self.ID = newID()
		self.speed = speed
		self.image = image
		self.height = image.get_rect().height
		self.pos = image.get_rect().move(0,self.height)
		
		# Defaults
		self.vertAnim = True
		self.horAnim = False
		self.animSpeed = 100
		self.animTimer = 0

		self.noAnim = False
	
	def update(self, delta):
		self.animTimer += delta
		if(self.animTimer >= self.animSpeed):
			self.anim()
			self.animTimer = 0

	def flipHoriz(self):
		self.image = pygame.transform.flip(self.image, True, False)

	def anim(self):
		if(self.noAnim):
			return
		self.image = pygame.transform.flip(self.image, self.vertAnim, self.horAnim)

	def move(self, x, y):
		if(x > 0):
			self.pos.left += self.speed
		if(y < 0):
			self.pos.top += self.speed
		if(x < 0):
			self.pos.left -= self.speed
		if(y > 0):
			self.pos.top -= self.speed


player = GameObject(playersurface, 2)
player.youDead = False
player.pos.left = 550
player.pos.top = 300
spawner = GameObject(spawnersurface, 2) 
spawner.pos.top = 400
spawner.noAnim = True
spawner.movingUp= True

def input(events):
	for event in events:
		if event.type == QUIT:
			sys.exit(0)
		#elif event.type == KEYDOWN:
	kb = pygame.key.get_pressed()
		
	if(kb[K_d]):
		if(player.pos.left+player.pos.width < 1024):
			player.move(1,0)
	elif(kb[K_a]):
		if(player.pos.left > 0):
			player.move(-1,0)

	if(kb[K_w]):
		if(player.pos.top > 0):
			player.move(0,1)
	elif(kb[K_s]):
		if(player.pos.top + player.pos.height < 768):
			player.move(0,-1)


def spawnerMove():
	if(spawner.movingUp):
		spawner.move(0,1)
	else:
		spawner.move(0,-1)
	
	if(spawner.pos.top < 0):
		spawner.movingUp = False
	elif(spawner.pos.top+spawner.height > 768):
		spawner.movingUp = True

#def movePython():

def movePython(py):
	collision = False
	if(py.pos.top < player.pos.top + player.pos.height and (py.pos.top + py.pos.height > player.pos.top)):
			collision = True

	if(py.pos.left + py.pos.width > player.pos.left and (py.pos.left < player.pos.left)):
			collision = True
	
	if(py.pos.left < player.pos.left + player.pos.width and (py.pos.left + py.pos.width > player.pos.left)):
			collision = True
	
	if(py.pos.top + py.pos.height > player.pos.top and (py.pos.top < player.pos.top)):
			collision = True
	
	if(py.pos.colliderect(player.pos)):
		player.youDead = True

	for other in pythons:
		if(py.ID == other.ID):
			continue
		if(py.pos.colliderect(other.pos)):
			py.movingUp = False if py.movingUp else True
	
#	Shitty python interaction code
#
#	for other in pythons:
#		if(py.ID == other.ID):
#			continue
#		if(py.pos.top + py.pos.height > other.pos.top + other.pos.height):
#			if(py.pos.top < other.pos.top+other.pos.height):
#				py.movingUp = False
#		if(py.pos.top < other.pos.top):
#			if(py.pos.top + py.pos.height > other.pos.top):
#				py.movingUp = True
#		
#		if(py.pos.left + py.pos.width > other.pos.left + other.pos.width):
#			if(py.pos.left < other.pos.left + other.pos.width):
#				py.movingLeft = False
#				py.flipHoriz()
#		if(py.pos.left < other.pos.left):
#			if(py.pos.left + py.pos.width > other.pos.left):
#				py.movingLeft = True
#				py.flipHoriz()

	if(py.pos.top < 0):
		py.movingUp = False
	elif(py.pos.top+py.height > 768):
		py.movingUp = True
	
	if(py.pos.left < 0):
		py.movingLeft = False
		py.flipHoriz()
	if(py.pos.left + py.pos.width > 1024):
		py.movingLeft = True
		py.flipHoriz()
	
	
	if(py.movingLeft):
		py.move(-1,0)
	else:
		py.move(1,0)

	if(py.movingUp):
		py.move(0,1)
	else:
		py.move(0,-1)
	
	

def createPython():
	python = GameObject(pythonsurface, 1)
	python.pos.left = spawner.pos.left + spawner.pos.width
	python.pos.top  = spawner.pos.top 
	python.horAnim = True
	python.vertAnim = False
	python.movingLeft = False
	python.movingUp = True if randrange(0,2) == 1 else False

	return python

pySpawnSpeed = 1000
pyTimer = 0

pythons = []

while True:
	# Timers
	delta = pygame.time.get_ticks() - lastFrame
	lastFrame = pygame.time.get_ticks()

	pyTimer += delta
	if(pyTimer >= pySpawnSpeed):
		pyTimer = 0
		pythons.append(createPython())

	# Input
	input(pygame.event.get())

	# Update
	player.update(delta)
	for py in pythons:
		movePython(py)
		py.update(delta)
	spawnerMove()
	
	# Draw
	screen.fill((0,0,0,0))
	screen.blit(player.image, player.pos )
	screen.blit(spawner.image, spawner.pos)

	for py in pythons:
		screen.blit(py.image, py.pos)

	pygame.display.flip()


	if(player.youDead):
		break

screen.fill((255,255,255,0))
font = pygame.font.Font(None,36)
text = font.render("You lose. Score: " + str(pygame.time.get_ticks()), 1, (10,10,10))
screen.blit(text, text.get_rect())
pygame.display.flip()

while True:
	for e in pygame.event.get():
		if e.type == QUIT:
			sys.exit(0)


"""Modulo de variables del entorno"""

import pygame

pygame.init() #Initialize pygame

#Colors
white = (255,255,255)
green = (0, 255, 0) 
blue = (0, 0, 128)  
black = (0,0,0)
gray = pygame.Color('gray12')
Color_line = (255,0,0)

### Valores de inicializacion ###
generation = 1
mutationRate = 90
FPS = 30
selectedCars = []
selected = 0
lines = True #If true then lines of player are shown
player = True #If true then player is shown
display_info = True #If true then display info is shown
frames = 0
maxspeed = 10 
number_track = 1


nnCars = [] #List of neural network cars
population = [] #Lista de individuos

num_of_nnCars = 50 #Number of neural network cars
alive = num_of_nnCars #Number of not collided (alive) cars
collidedCars = [] #List containing collided cars   
selected = 0


white_small_car = pygame.image.load('Images\Sprites\white_small.png')
white_big_car = pygame.image.load('Images\Sprites\white_big.png')
green_small_car = pygame.image.load('Images\Sprites\green_small.png')
green_big_car = pygame.image.load('Images\Sprites\green_big.png')
blue_small_car = pygame.image.load(r'Images\Sprites\blue_small.png')
blue_big_car = pygame.image.load(r'Images\Sprites\blue_big.png')

bg = pygame.image.load('bg7.png')
bg4 = pygame.image.load('bg4.png')

img = 0 #This one is used when recording frames
size = width,height = 1600, 900 #Size to use when creating pygame window

# Tasas de mutacion
mutation_rates = {ord("0"): 0, ord("1"): 10, ord("2"): 20, ord("3"): 30, ord("4"): 40, ord("5"): 50, ord("6"): 60, ord("7"): 70, ord("8"): 80, ord("9"): 90}

# Arquitectura redes neuronales
inputLayer = 6
hiddenLayer = 6
outputLayer = 4

# Textos y su ubicacion en pantalla
font = pygame.font.Font('freesansbold.ttf', 18)

#These is just the text being displayed on pygame window
infoX = 1265
infoY = 600

text1 = font.render('0..9 - Change Mutation', True, white)
text2 = font.render('LMB - Select/Unselect', True, white)
text3 = font.render('RMB - Delete', True, white)
text4 = font.render('L - Show/Hide Lines', True, white)
text5 = font.render('R - Reset', True, white)
text6 = font.render('B - Breed', True, white)
text7 = font.render('C - Clean', True, white)
text8 = font.render('N - Next Track', True, white)
text9 = font.render('P - Toggle Player', True, white)
text10 = font.render('D - Toggle Info', True, white)
text11 = font.render('M - Breed and Next Track', True, white)
text12 = font.render('A - Automatic Process', True, white)

text1Rect = text1.get_rect().move(infoX,infoY)
text2Rect = text2.get_rect().move(infoX,infoY+text1Rect.height)
text3Rect = text3.get_rect().move(infoX,infoY+2*text1Rect.height)
text4Rect = text4.get_rect().move(infoX,infoY+3*text1Rect.height)
text5Rect = text5.get_rect().move(infoX,infoY+4*text1Rect.height)
text6Rect = text6.get_rect().move(infoX,infoY+5*text1Rect.height)
text7Rect = text7.get_rect().move(infoX,infoY+6*text1Rect.height)
text8Rect = text8.get_rect().move(infoX,infoY+7*text1Rect.height)
text9Rect = text9.get_rect().move(infoX,infoY+8*text1Rect.height)
text10Rect = text10.get_rect().move(infoX,infoY+9*text1Rect.height)
text11Rect = text11.get_rect().move(infoX,infoY+10*text1Rect.height)
text12Rect = text12.get_rect().move(infoX,infoY+11*text1Rect.height)


gameDisplay = pygame.display.set_mode(size) #creates screen
clock = pygame.time.Clock()

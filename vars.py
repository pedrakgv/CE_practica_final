import pygame
#Colors
white = (255,255,255)
green = (0, 255, 0) 
blue = (0, 0, 128)  
black = (0,0,0)
gray = pygame.Color('gray12')
Color_line = (255,0,0)

### VALORES DE INICIALIZACION ###
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
num_of_nnCars = 50 #Number of neural network cars
alive = num_of_nnCars #Number of not collided (alive) cars
collidedCars = [] #List containing collided cars   
selected = 0


white_small_car = pygame.image.load('Images\Sprites\white_small.png')
white_big_car = pygame.image.load('Images\Sprites\white_big.png')
green_small_car = pygame.image.load('Images\Sprites\green_small.png')
green_big_car = pygame.image.load('Images\Sprites\green_big.png')

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


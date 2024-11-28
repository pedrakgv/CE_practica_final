import pygame
import random
import os
import math
import numpy as np
import time
import sys
from datetime import datetime
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from operator import attrgetter

from vars import *
# from coche import Coche
from grid import Cell, Maze, generateRandomMap
from cruces import uniformCrossOverBiases, uniformCrossOverWeights
from mutaciones import mutateOneBiasesGene, mutateOneWeightGene

pygame.init() #Initialize pygame
#Some variables initializations

#These is just the text being displayed on pygame window
infoX = 1265
infoY = 600 
font = pygame.font.Font('freesansbold.ttf', 18)
text1 = font.render('0..9 - Change Mutation', True, white)
text2 = font.render('LMB - Select/Unselect', True, white)
text3 = font.render('RMB - Delete', True, white)
text4 = font.render('L - Show/Hide Lines', True, white)
text5 = font.render('R - Reset', True, white)
text6 = font.render('B - Breed', True, white)
text7 = font.render('C - Clean', True, white)
text8 = font.render('N - Next Track', True, white)
text9 = font.render('A - Toggle Player', True, white)
text10 = font.render('D - Toggle Info', True, white)
text11 = font.render('M - Breed and Next Track', True, white)
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


def displayTexts():  
    infotextX = 100
    infotextY = 700
    infotext1 = font.render('Gen ' + str(generation), True, white) 
    infotext2 = font.render('Cars: ' + str(num_of_nnCars), True, white)
    infotext3 = font.render('Alive: ' + str(alive), True, white)
    infotext4 = font.render('Selected: ' + str(selected), True, white)
    if lines == True:
        infotext5 = font.render('Lines ON', True, white)
    else:
        infotext5 = font.render('Lines OFF', True, white)
    if player == True:
        infotext6 = font.render('Player ON', True, white)
    else:
        infotext6 = font.render('Player OFF', True, white)
    #infotext7 = font.render('Mutation: '+ str(2*mutationRate), True, white)
    #infotext8 = font.render('Frames: ' + str(frames), True, white)
    infotext9 = font.render('FPS: 30', True, white)
    infotext1Rect = infotext1.get_rect().move(infotextX,infotextY)
    infotext2Rect = infotext2.get_rect().move(infotextX,infotextY+infotext1Rect.height)
    infotext3Rect = infotext3.get_rect().move(infotextX,infotextY+2*infotext1Rect.height)
    infotext4Rect = infotext4.get_rect().move(infotextX,infotextY+3*infotext1Rect.height)
    infotext5Rect = infotext5.get_rect().move(infotextX,infotextY+4*infotext1Rect.height)
    infotext6Rect = infotext6.get_rect().move(infotextX,infotextY+5*infotext1Rect.height)
    #infotext7Rect = infotext7.get_rect().move(infotextX,infotextY+6*infotext1Rect.height)
    #infotext8Rect = infotext8.get_rect().move(infotextX,infotextY+7*infotext1Rect.height)
    infotext9Rect = infotext9.get_rect().move(infotextX,infotextY+6*infotext1Rect.height)

    gameDisplay.blit(text1, text1Rect)  
    gameDisplay.blit(text2, text2Rect)  
    gameDisplay.blit(text3, text3Rect) 
    gameDisplay.blit(text4, text4Rect) 
    gameDisplay.blit(text5, text5Rect) 
    gameDisplay.blit(text6, text6Rect)
    gameDisplay.blit(text7, text7Rect)   
    gameDisplay.blit(text8, text8Rect)  
    gameDisplay.blit(text9, text9Rect)     
    gameDisplay.blit(text10, text10Rect) 
    gameDisplay.blit(text11, text11Rect)  
    
    gameDisplay.blit(infotext1, infotext1Rect)  
    gameDisplay.blit(infotext2, infotext2Rect)  
    gameDisplay.blit(infotext3, infotext3Rect) 
    gameDisplay.blit(infotext4, infotext4Rect) 
    gameDisplay.blit(infotext5, infotext5Rect) 
    gameDisplay.blit(infotext6, infotext6Rect)
    #gameDisplay.blit(infotext7, infotext7Rect) 
    #gameDisplay.blit(infotext8, infotext8Rect) 
    gameDisplay.blit(infotext9, infotext9Rect) 
    return
 

gameDisplay = pygame.display.set_mode(size) #creates screen
clock = pygame.time.Clock()

import numpy as np
import math
import pygame

import vars
from acciones import move, rotation, calculateDistance, sigmoid

class Coche:
  def __init__(self, sizes):
    self.score = 0
    self.num_layers = len(sizes) #Number of nn layers
    self.sizes = sizes #List with number of neurons per layer
    self.biases = [np.random.randn(y, 1) for y in sizes[1:]] #Biases
    self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])] #Weights 
    #c1, c2, c3, c4, c5 are five 2D points where the car could collided, updated in every frame
    self.c1 = 0,0
    self.c2 = 0,0
    self.c3 = 0,0
    self.c4 = 0,0
    self.c5 = 0,0
    #d1, d2, d3, d4, d5 are distances from the car to those points, updated every frame too and used as the input for the NN
    self.d1 = 0
    self.d2 = 0
    self.d3 = 0
    self.d4 = 0
    self.d5 = 0
    self.yaReste = False
    #The input and output of the NN must be in a numpy array format
    self.inp = np.array([[self.d1],[self.d2],[self.d3],[self.d4],[self.d5]])
    self.outp = np.array([[0],[0],[0],[0]])
    #Boolean used for toggling distance lines
    self.showlines = False
    #Initial location of the car
    self.x = 120
    self.y = 480
    self.center = self.x, self.y
    #Height and width of the car
    self.height = 35 #45
    self.width = 17 #25
    #These are the four corners of the car, using polygon instead of rectangle object, when rotating or moving the car, we rotate or move these
    self.d = self.x-(self.width/2),self.y-(self.height/2)
    self.c = self.x + self.width-(self.width/2), self.y-(self.height/2)
    self.b = self.x + self.width-(self.width/2), self.y + self.height-(self.height/2) #El rectangulo está centrado en (x,y)
    self.a = self.x-(self.width/2), self.y + self.height-(self.height/2)              #(a), (b), (c), (d) son los vertices
    #Velocity, acceleration and direction of the car
    self.velocity = 0
    self.acceleration = 0  
    self.angle = 180
    #Boolean which goes true when car collides
    self.collided = False
    #Car color and image
    self.color = white
    self.car_image = white_small_car
  def set_accel(self, accel): 
    self.acceleration = accel
  def rotate(self, rot): 
    self.angle += rot
    if self.angle > 360:
        self.angle = 0
    if self.angle < 0:
        self.angle = 360 + self.angle
  def update(self): #En cada frame actualizo los vertices (traslacion y rotacion) y los puntos de colision
    self.score += self.velocity
    if self.acceleration != 0:
        self.velocity += self.acceleration
        if self.velocity > maxspeed:
            self.velocity = maxspeed
        elif self.velocity < 0:
            self.velocity = 0
    else:
        self.velocity *= 0.92
        
    self.x, self.y = move((self.x, self.y), self.angle, self.velocity)
    self.center = self.x, self.y
    
    self.d = self.x-(self.width/2),self.y-(self.height/2)
    self.c = self.x + self.width-(self.width/2), self.y-(self.height/2)
    self.b = self.x + self.width-(self.width/2), self.y + self.height-(self.height/2) #El rectangulo está centrado en (x,y)
    self.a = self.x-(self.width/2), self.y + self.height-(self.height/2)              #(a), (b), (c), (d) son los vertices
        
    self.a = rotation((self.x,self.y), self.a, math.radians(self.angle)) 
    self.b = rotation((self.x,self.y), self.b, math.radians(self.angle))  
    self.c = rotation((self.x,self.y), self.c, math.radians(self.angle))  
    self.d = rotation((self.x,self.y), self.d, math.radians(self.angle))    
    
    self.c1 = move((self.x,self.y),self.angle,10)
    while bg4.get_at((int(self.c1[0]),int(self.c1[1]))).a!=0:
        self.c1 = move((self.c1[0],self.c1[1]),self.angle,10)
    while bg4.get_at((int(self.c1[0]),int(self.c1[1]))).a==0:
        self.c1 = move((self.c1[0],self.c1[1]),self.angle,-1)

    self.c2 = move((self.x,self.y),self.angle+45,10)
    while bg4.get_at((int(self.c2[0]),int(self.c2[1]))).a!=0:
        self.c2 = move((self.c2[0],self.c2[1]),self.angle+45,10)
    while bg4.get_at((int(self.c2[0]),int(self.c2[1]))).a==0:
        self.c2 = move((self.c2[0],self.c2[1]),self.angle+45,-1)

    self.c3 = move((self.x,self.y),self.angle-45,10)
    while bg4.get_at((int(self.c3[0]),int(self.c3[1]))).a!=0:
        self.c3 = move((self.c3[0],self.c3[1]),self.angle-45,10)
    while bg4.get_at((int(self.c3[0]),int(self.c3[1]))).a==0:
        self.c3 = move((self.c3[0],self.c3[1]),self.angle-45,-1)
        
    self.c4 = move((self.x,self.y),self.angle+90,10)
    while bg4.get_at((int(self.c4[0]),int(self.c4[1]))).a!=0:
        self.c4 = move((self.c4[0],self.c4[1]),self.angle+90,10)
    while bg4.get_at((int(self.c4[0]),int(self.c4[1]))).a==0:
        self.c4 = move((self.c4[0],self.c4[1]),self.angle+90,-1)
        
    self.c5 = move((self.x,self.y),self.angle-90,10)
    while bg4.get_at((int(self.c5[0]),int(self.c5[1]))).a!=0:
        self.c5 = move((self.c5[0],self.c5[1]),self.angle-90,10)
    while bg4.get_at((int(self.c5[0]),int(self.c5[1]))).a==0:
        self.c5 = move((self.c5[0],self.c5[1]),self.angle-90,-1)
        
    self.d1 = int(calculateDistance(self.center[0], self.center[1], self.c1[0], self.c1[1]))
    self.d2 = int(calculateDistance(self.center[0], self.center[1], self.c2[0], self.c2[1]))
    self.d3 = int(calculateDistance(self.center[0], self.center[1], self.c3[0], self.c3[1]))
    self.d4 = int(calculateDistance(self.center[0], self.center[1], self.c4[0], self.c4[1]))
    self.d5 = int(calculateDistance(self.center[0], self.center[1], self.c5[0], self.c5[1]))
    
    

  def draw(self,display):
    rotated_image = pygame.transform.rotate(self.car_image, -self.angle-180)
    rect_rotated_image = rotated_image.get_rect()
    rect_rotated_image.center = self.x, self.y
    gameDisplay.blit(rotated_image, rect_rotated_image)
  
    center = self.x, self.y
    if self.showlines: 
        pygame.draw.line(gameDisplay,Color_line,(self.x,self.y),self.c1,2)
        pygame.draw.line(gameDisplay,Color_line,(self.x,self.y),self.c2,2)
        pygame.draw.line(gameDisplay,Color_line,(self.x,self.y),self.c3,2)
        pygame.draw.line(gameDisplay,Color_line,(self.x,self.y),self.c4,2)
        pygame.draw.line(gameDisplay,Color_line,(self.x,self.y),self.c5,2) 
    
  def showLines(self):
    self.showlines = not self.showlines
    
  def feedforward(self):
    #Return the output of the network
    self.inp = np.array([[self.d1],[self.d2],[self.d3],[self.d4],[self.d5],[self.velocity]])
    for b, w in zip(self.biases, self.weights):
        self.inp = sigmoid(np.dot(w, self.inp)+b)
    self.outp = self.inp
    return self.outp
  
  def collision(self):
      if (bg4.get_at((int(self.a[0]),int(self.a[1]))).a==0) or (bg4.get_at((int(self.b[0]),int(self.b[1]))).a==0) or (bg4.get_at((int(self.c[0]),int(self.c[1]))).a==0) or (bg4.get_at((int(self.d[0]),int(self.d[1]))).a==0):
        return True
      else:
        return False

  def resetPosition(self):
      self.x = 120
      self.y = 480
      self.angle = 180
      return
      
  def takeAction(self): 
    if self.outp.item(0) > 0.5: #Accelerate
        self.set_accel(0.2)
    else:
        self.set_accel(0)      
    if self.outp.item(1) > 0.5: #Brake
        self.set_accel(-0.2)     
    if self.outp.item(2) > 0.5: #Turn right
        self.rotate(-5)    
    if self.outp.item(3) > 0.5: #Turn left
        self.rotate(5) 
    return
  

car = Coche([inputLayer, hiddenLayer, outputLayer])
auxcar = Coche([inputLayer, hiddenLayer, outputLayer])

for i in range(num_of_nnCars):
	nnCars.append(Coche([inputLayer, hiddenLayer, outputLayer]))
   
def redrawGameWindow(): #Called on very frame   

    global alive  
    global frames
    global img
    
    frames += 1

    gameD = gameDisplay.blit(bg, (0,0))  
       
    #NN cars
    for nncar in nnCars:
        if not nncar.collided:
            nncar.update() #Update: Every car center coord, corners, directions, collision points and collision distances
        
        if nncar.collision(): #Check which car collided
            nncar.collided = True #If collided then change collided attribute to true
            if nncar.yaReste == False:
                alive -= 1
                nncar.yaReste = True

        else: #If not collided then feedforward the input and take an action
            nncar.feedforward()
            nncar.takeAction()
        nncar.draw(gameDisplay)
    

    #Same but for player
    if player:
        car.update()
        if car.collision():
            car.resetPosition()
            car.update()
        car.draw(gameDisplay)    
    if display_info:    
        displayTexts() 
    pygame.display.update() #updates the screen
    #Take a screenshot of every frame
    #pygame.image.save(gameDisplay, "pygameVideo/screenshot" + str(img) + ".jpeg")
    #img += 1
    
while True:
    #now1 = time.time()  
  
    for event in pygame.event.get(): #Check for events
        if event.type == pygame.QUIT:
            pygame.quit() #quits
            quit()
            
        if event.type == pygame.KEYDOWN: #If user uses the keyboard
            if event.key == ord ( "l" ): #If that key is l
                car.showLines()
                lines = not lines
            if event.key == ord ( "c" ): #If that key is c
                for nncar in nnCars:
                    if nncar.collided == True:
                        nnCars.remove(nncar)
                        if nncar.yaReste == False:
                            alive -= 1
            if event.key == ord ( "a" ): #If that key is a
                player = not player
            if event.key == ord ( "d" ): #If that key is d
                display_info = not display_info
            if event.key == ord ( "n" ): #If that key is n
                number_track = 2
                # print(number_track)
                for nncar in nnCars:
                    nncar.velocity = 0
                    nncar.acceleration = 0
                    nncar.x = 140
                    nncar.y = 610
                    nncar.angle = 180
                    nncar.collided = False
                generateRandomMap(gameDisplay)
                bg = pygame.image.load('randomGeneratedTrackFront.png')
                bg4 = pygame.image.load('randomGeneratedTrackBack.png')


            # Selección Manual
            if event.key == ord ( "b" ):
                if (len(selectedCars) == 2):
                    for nncar in nnCars:
                        nncar.score = 0
               
                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    nnCars.clear() 
                    
                    for i in range(num_of_nnCars):
                        nnCars.append(Coche([inputLayer, hiddenLayer, outputLayer]))
                        
                    for i in range(0,num_of_nnCars-2,2):
                        uniformCrossOverWeights(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
                        uniformCrossOverBiases(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
                    
                    nnCars[num_of_nnCars-2] = selectedCars[0]
                    nnCars[num_of_nnCars-1] = selectedCars[1]
                    
                    nnCars[num_of_nnCars-2].car_image = green_small_car
                    nnCars[num_of_nnCars-1].car_image = green_small_car
                    
                    nnCars[num_of_nnCars-2].resetPosition()
                    nnCars[num_of_nnCars-1].resetPosition()
                    
                    nnCars[num_of_nnCars-2].collided = False
                    nnCars[num_of_nnCars-1].collided = False
                                  
                    for i in range(num_of_nnCars-2):
                        for j in range(mutationRate):
                            mutateOneWeightGene(nnCars[i], auxcar)
                            mutateOneWeightGene(auxcar, nnCars[i])
                            mutateOneBiasesGene(nnCars[i], auxcar)
                            mutateOneBiasesGene(auxcar, nnCars[i])
                    if number_track != 1:
                        for nncar in nnCars:
                            nncar.x = 140
                            nncar.y = 610 
                      
                    selectedCars.clear()
                    
                
            if event.key == ord ( "m" ):
                if (len(selectedCars) == 2):
                    for nncar in nnCars:
                        nncar.score = 0
                   
                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    nnCars.clear() 
                    
                    for i in range(num_of_nnCars):
                        nnCars.append(Coche([inputLayer, hiddenLayer, outputLayer]))
                        
                    for i in range(0,num_of_nnCars-2,2):
                        uniformCrossOverWeights(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
                        uniformCrossOverBiases(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
                    
                    nnCars[num_of_nnCars-2] = selectedCars[0]
                    nnCars[num_of_nnCars-1] = selectedCars[1]
                    
                    nnCars[num_of_nnCars-2].car_image = green_small_car
                    nnCars[num_of_nnCars-1].car_image = green_small_car
                    
                    nnCars[num_of_nnCars-2].resetPosition()
                    nnCars[num_of_nnCars-1].resetPosition()
                    
                    nnCars[num_of_nnCars-2].collided = False
                    nnCars[num_of_nnCars-1].collided = False
                                  
                    for i in range(num_of_nnCars-2):
                        for j in range(mutationRate):
                            mutateOneWeightGene(nnCars[i], auxcar)
                            mutateOneWeightGene(auxcar, nnCars[i])
                            mutateOneBiasesGene(nnCars[i], auxcar)
                            mutateOneBiasesGene(auxcar, nnCars[i])

                    for nncar in nnCars:
                        nncar.x = 140
                        nncar.y = 610 
                      
                    selectedCars.clear()
                    
                    number_track = 2
                    # print(number_track)
                    for nncar in nnCars:
                        nncar.velocity = 0
                        nncar.acceleration = 0
                        nncar.x = 140
                        nncar.y = 610
                        nncar.angle = 180
                        nncar.collided = False
                    generateRandomMap(gameDisplay)
                    bg = pygame.image.load('randomGeneratedTrackFront.png')
                    bg4 = pygame.image.load('randomGeneratedTrackBack.png')
            if event.key == ord ( "r" ):
                generation = 1
                alive = num_of_nnCars
                nnCars.clear() 
                selectedCars.clear()
                for i in range(num_of_nnCars):
                    nnCars.append(Coche([inputLayer, hiddenLayer, outputLayer]))
                for nncar in nnCars:
                    if number_track == 1:
                        nncar.x = 120
                        nncar.y = 480
                    elif number_track == 2:
                        nncar.x = 100
                        nncar.y = 300
            if event.key in mutation_rates:
                mutationRate = mutation_rates[event.key]

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #This returns a tuple:
            #(leftclick, middleclick, rightclick)
            #Each one is a boolean integer representing button up/down.
            mouses = pygame.mouse.get_pressed()
            if mouses[0]:
                pos = pygame.mouse.get_pos()
                point = Point(pos[0], pos[1])
                #Revisar la lista de autos y ver cual estaba ahi
                for nncar in nnCars:  
                    polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
                    if (polygon.contains(point)):
                        if nncar in selectedCars:
                            selectedCars.remove(nncar)
                            selected -= 1
                            if nncar.car_image == white_big_car:
                                nncar.car_image = white_small_car 
                            if nncar.car_image == green_big_car:
                                nncar.car_image = green_small_car
                            if nncar.collided:
                                nncar.velocity = 0
                                nncar.acceleration = 0
                            nncar.update()
                        else:
                            if len(selectedCars) < 2:
                                selectedCars.append(nncar)
                                selected +=1
                                if nncar.car_image == white_small_car:
                                    nncar.car_image = white_big_car  
                                if nncar.car_image == green_small_car:
                                    nncar.car_image = green_big_car  
                                if nncar.collided:
                                    nncar.velocity = 0
                                    nncar.acceleration = 0
                                nncar.update()
                        break
            
    
            if mouses[2]:
                pos = pygame.mouse.get_pos()
                point = Point(pos[0], pos[1])
                for nncar in nnCars:  
                    polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
                    if (polygon.contains(point)):
                        if nncar not in selectedCars:
                            nnCars.remove(nncar)
                            alive -= 1
                        break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.rotate(-5)
    if keys[pygame.K_RIGHT]:
        car.rotate(5)
    if keys[pygame.K_UP]:
        car.set_accel(0.2)
    else:
        car.set_accel(0)
    if keys[pygame.K_DOWN]:
        car.set_accel(-0.2)
      
    redrawGameWindow()   
    
    clock.tick(FPS)
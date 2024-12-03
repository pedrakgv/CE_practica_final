"""Modulo de la clase Coche"""
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
        self.color = vars.white
        self.car_image = vars.white_small_car

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
            if self.velocity > vars.maxspeed:
                self.velocity = vars.maxspeed
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
        while vars.bg4.get_at((int(self.c1[0]),int(self.c1[1]))).a!=0:
            self.c1 = move((self.c1[0],self.c1[1]),self.angle,10)
        while vars.bg4.get_at((int(self.c1[0]),int(self.c1[1]))).a==0:
            self.c1 = move((self.c1[0],self.c1[1]),self.angle,-1)

        self.c2 = move((self.x,self.y),self.angle+45,10)
        while vars.bg4.get_at((int(self.c2[0]),int(self.c2[1]))).a!=0:
            self.c2 = move((self.c2[0],self.c2[1]),self.angle+45,10)
        while vars.bg4.get_at((int(self.c2[0]),int(self.c2[1]))).a==0:
            self.c2 = move((self.c2[0],self.c2[1]),self.angle+45,-1)

        self.c3 = move((self.x,self.y),self.angle-45,10)
        while vars.bg4.get_at((int(self.c3[0]),int(self.c3[1]))).a!=0:
            self.c3 = move((self.c3[0],self.c3[1]),self.angle-45,10)
        while vars.bg4.get_at((int(self.c3[0]),int(self.c3[1]))).a==0:
            self.c3 = move((self.c3[0],self.c3[1]),self.angle-45,-1)
            
        self.c4 = move((self.x,self.y),self.angle+90,10)
        while vars.bg4.get_at((int(self.c4[0]),int(self.c4[1]))).a!=0:
            self.c4 = move((self.c4[0],self.c4[1]),self.angle+90,10)
        while vars.bg4.get_at((int(self.c4[0]),int(self.c4[1]))).a==0:
            self.c4 = move((self.c4[0],self.c4[1]),self.angle+90,-1)
            
        self.c5 = move((self.x,self.y),self.angle-90,10)
        while vars.bg4.get_at((int(self.c5[0]),int(self.c5[1]))).a!=0:
            self.c5 = move((self.c5[0],self.c5[1]),self.angle-90,10)
        while vars.bg4.get_at((int(self.c5[0]),int(self.c5[1]))).a==0:
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
        vars.gameDisplay.blit(rotated_image, rect_rotated_image)
    
        center = self.x, self.y
        if self.showlines: 
            pygame.draw.line(vars.gameDisplay,vars.Color_line,(self.x,self.y),self.c1,2)
            pygame.draw.line(vars.gameDisplay,vars.Color_line,(self.x,self.y),self.c2,2)
            pygame.draw.line(vars.gameDisplay,vars.Color_line,(self.x,self.y),self.c3,2)
            pygame.draw.line(vars.gameDisplay,vars.Color_line,(self.x,self.y),self.c4,2)
            pygame.draw.line(vars.gameDisplay,vars.Color_line,(self.x,self.y),self.c5,2) 
        
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
        if (vars.bg4.get_at((int(self.a[0]),int(self.a[1]))).a==0) or (vars.bg4.get_at((int(self.b[0]),int(self.b[1]))).a==0) or (vars.bg4.get_at((int(self.c[0]),int(self.c[1]))).a==0) or (vars.bg4.get_at((int(self.d[0]),int(self.d[1]))).a==0):
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
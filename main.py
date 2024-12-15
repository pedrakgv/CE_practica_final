"""Modulo principal"""

import pygame
import math
import numpy as np

from vars import *
from coche import Coche
from grid import generateRandomMap
from cruces import uniformCrossOverBiases, uniformCrossOverWeights, uniformCrossOver, combinedCrossOver, morphologicalCrossOver
from mutaciones import mutateOneBiasesGene, mutateOneWeightGene
from seleccion import seleccion_manual_individuo, eliminacion_manual_individuo
from pantalla import displayTexts
from acciones import move, rotation, calculateDistance, sigmoid


class Coche:
  def __init__(self, genome = []):
    sizes = [inputLayer, hiddenLayer, outputLayer]
    self.score = 0
    self.num_layers = len(sizes) #Number of nn layers
    self.sizes = sizes #List with number of neurons per layer
    self.vueltas = 0 # Numero de vueltas
    self.line_state = "before_line"  # Estado inicial: antes de la línea
    self.previous_line_state = "before_line"  # Estado anterior
    self.passed_halfway = False  # Indica si el coche ha pasado la mitad del circuito

    
    if np.size(genome) == 0:
        biases = np.random.randn(sum(sizes[1:]))
        weights = np.random.randn(sum(y * x for x, y in zip(sizes[:-1], sizes[1:])))

        genome = np.concatenate((biases, weights))
    
    self.update_car(genome)
    
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
    
  def update_car(self, genome):
    """
    Reconstruye bias y weights con el cromosoma (genome) completo
    """
    self.biases = []
    idx = 0
    for y in self.sizes[1:]:
        self.biases.append(np.array(genome[idx:idx + y]).reshape(y, 1))
        idx += y

    # Reconstrucción de weights
    self.weights = []
    for x, y in zip(self.sizes[:-1], self.sizes[1:]):
        self.weights.append(np.array(genome[idx:idx + y * x]).reshape(y, x))
        idx += y * x

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
  
#   def check_goal(self): # Rango meta eje x: 74-165 eje y: 418-424
#     # Verificar si el coche está en la meta y aumentar el contador de vueltas
#     # print(self.x, self.y)
#     if 74 <= self.x <= 165 and 420 <= self.y <= 424:
#         self.vueltas += 1
#         print("META ALCANZADA") 
#     return self.vueltas

  def check_goal(self, line_coords, halfway_x):
    """Metodo para verificar si un individuo ha llegado a la solucion, en este caso si un coche llega a la meta"""
    x_min, x_max = line_coords["x_range"]  # Rango del eje X de la meta
    y_min, y_max = line_coords["y_range"]  # Rango del eje Y de la meta

    # Verificar si el coche ha pasado la mitad del circuito
    if self.x > halfway_x and not self.passed_halfway:
        self.passed_halfway = True
        print("Coche ha pasado la mitad del circuito.")

    # Verificar si el coche está dentro del rango de la meta (en ambos ejes) Y ha pasado la mitad del circuito
    if self.passed_halfway and x_min <= self.x <= x_max and y_min <= self.y <= y_max:
        self.vueltas += 1
        print(f"Meta alcanzada, vueltas: {self.vueltas}")
        self.passed_halfway = False  # Reiniciar la marca de haber pasado la mitad
        return True

    return False

def redrawGameWindow(): #Called on very frame   
    
    global alive  
    global frames
    global img
    
    frames += 1

    gameD = gameDisplay.blit(bg, (0,0))  
    

    #NN cars
    for nncar in nnCars:
        # line_coords = {"x_range": (74, 165), "y_range": (410, 434)}

        if not nncar.collided:
            nncar.update() #Update: Every car center coord, corners, directions, collision points and collision distances
            nncar.check_goal(line_coords, 800)
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
        car.check_goal(line_coords, 800)
        # print(car.x, car.y)
        if car.collision():
            car.resetPosition()
            car.update()
            car.check_goal(line_coords, 800)
        car.draw(gameDisplay)    
    if display_info:    
        displayTexts() 
    pygame.display.update() #updates the screen
    #Take a screenshot of every frame
    #pygame.image.save(gameDisplay, "pygameVideo/screenshot" + str(img) + ".jpeg")
    #img += 1


car = Coche()
auxcar = Coche()

sizes = [inputLayer, hiddenLayer, outputLayer]

biases = np.random.randn(sum(sizes[1:]))
weights = np.random.randn(sum(y * x for x, y in zip(sizes[:-1], sizes[1:])))

genome = np.concatenate((biases, weights))


#Generación de la población inicial

for i in range(num_of_nnCars):
    
    #Generación de individuos con codificación real
    #Estructura: primero los bias, después los pesos de cada capa en orden
    biases = np.random.randn(sum(sizes[1:]))
    weights = np.random.randn(sum(y * x for x, y in zip(sizes[:-1], sizes[1:])))

    genome = np.concatenate((biases, weights))


    population.append(genome)
    nnCars.append(Coche(genome))
   



while True:
    #now1 = time.time()  
  
    for event in pygame.event.get(): #Check for events
        if event.type == pygame.QUIT:
            pygame.quit() #quits
            quit()
            
        if event.type == pygame.KEYDOWN: #If user uses the keyboard

            if event.key == ord ( "a" ): #Proceso automatico
                print("Proceso automatico")
                gen_contador = 0
                solucion = None

                while gen_contador < generaciones:
                    print(f"Generación {gen_contador + 1}")
                    
                    # 1. **Evaluación**
                    nnCars.clear()
                    for ind in population:      # Crear decodificaciones de los individuos, en este caso coches
                        nnCars.append(Coche(ind))

                    if gen_contador > 0:
                        # Asignar imágenes para padres
                        for i in range(len(top2_parents)):  # cruce morfológico: top5_parents
                            nnCars[i].car_image = green_small_car  # Imagen para los padres

                        # Asignar imágenes para hijos
                        for i in range(len(top2_parents), len(top2_parents) + 2):  # cruce morfológico: top5_parents
                            nnCars[i].car_image = blue_small_car  # Imagen para los hijos
                    
                    for _ in range(100):  # 1000 frames
                        redrawGameWindow()
                        clock.tick(FPS)

                    # Fitness
                    # for i in range(num_of_nnCars):
                    #     valores_fitness[i], es_solucion = calcularFitness(nnCars[i])
                                        # if coche.check_goal(line_coords, 800):
                                        #         # El coche alcanza la meta, encontrando la solucion
                    #     if es_solucion:
                    #         solucion = nnCars[i]
                    #         break

                    #temporal
                    valores_fitness = list(range(1, num_of_nnCars + 1))

                    if solucion:
                        print("Se ha encontrado una solución")
                        break

                    # 2. **Selección**

                    # Selección basada en el score: elige los dos mejores
                    top2_indices = sorted(range(len(valores_fitness)), key=lambda i: valores_fitness[i], reverse=True)[:2]
                    top2_parents = [population[i] for i in top2_indices]

                    
                        
                    print(f"Seleccionados para cruce: {top2_indices[0]} y {top2_indices[1]} con puntuaciones {valores_fitness[top2_indices[0]]} y {valores_fitness[top2_indices[1]]}")

                    # 3. **Cruce**
                    # child1_genome, child2_genome = uniformCrossOver(top2_parents_genomes[0], top2_parents_genomes[1]) # cruce uniforme
                    child1_genome, child2_genome = combinedCrossOver(top2_parents[0], top2_parents[1], alpha=0.3)  # cruce combinado

                    # seleccionar 5 padres para cruce morfológico
                    # top5_parents = sorted_nnCars[:5]
                    # top5_parents_genomes = [population[nnCars.index(parent)] for parent in top5_parents]
                    # child1_genome, child2_genome = morphologicalCrossOver(top5_parents_genomes)  # cruce morfológico

                    # # 4. **Mutación**
                    # child1_genome = mutate_genome(child1_genome)
                    # child2_genome = mutate_genome(child2_genome)

                    # 5. **Reemplazo**
                    # Limpiar población existente y añadir nueva generación
                    population.clear()

                    # Añadir los padres y los hijos
                    population.extend(top2_parents)  # cruce morfológico: top5_parents_genomes
                    population.append(child1_genome)
                    population.append(child2_genome)


                    # Rellenar la población con nuevos individuos aleatorios
                    for _ in range(num_of_nnCars - 4):
                        biases = np.random.randn(sum(sizes[1:]))
                        weights = np.random.randn(sum(y * x for x, y in zip(sizes[:-1], sizes[1:])))
                        genome = np.concatenate((biases, weights))
                        population.append(genome)


                    if number_track != 1:
                        for nncar in nnCars:
                            nncar.x = 140
                            nncar.y = 610

                    
                    gen_contador += 1

                if solucion:
                    print(f"Proceso terminado. El ganador es {solucion}")
                else:
                    print("Proceso terminado. No se encontró un ganador.")


            if event.key == ord ( "l" ): #If that key is l
                car.showLines()
                lines = not lines
            # if event.key == ord ( "c" ): #If that key is c
            #     for nncar in nnCars:
            #         if nncar.collided == True:
            #             nnCars.remove(nncar)
            #             if nncar.yaReste == False:
            #                 alive -= 1
            if event.key == ord ( "p" ): #If that key is a
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

            #Selección Manual
            if event.key == ord ( "b" ):       # B: Cruce con codificacion real
                if (len(selectedCars) == 2):
                    for nncar in nnCars:
                        nncar.score = 0
               
                    #print("Poblacion antes del cruce: ", len(nnCars), len(population))

                    
                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    
                    parent1_index = nnCars.index(selectedCars[0])
                    parent2_index = nnCars.index(selectedCars[1])

                    parent1_genome = population[parent1_index]
                    parent2_genome = population[parent2_index]

                    nnCars.clear() 
                    population.clear()

                    # child1_genome, child2_genome = uniformCrossOver(parent1_genome, parent2_genome)  # cruce uniforme
                    child1_genome, child2_genome = combinedCrossOver(parent1_genome, parent2_genome, alpha=0.2)  # cruce combinado

                    #De momento se añade a la siguiente generacion tanto los padres como los hijos
                    population.append(parent1_genome)
                    population.append(parent2_genome)
                    nnCars.append(Coche(parent1_genome))
                    nnCars.append(Coche(parent2_genome))
                    
                    population.append(child1_genome)
                    population.append(child2_genome)
                    nnCars.append(Coche(child1_genome))
                    nnCars.append(Coche(child2_genome))
                    
                    
                    nnCars[0].car_image = green_small_car #Padre 1
                    nnCars[1].car_image = green_small_car #Padre 2
                    nnCars[2].car_image = blue_small_car #Hijo 1
                    nnCars[3].car_image = blue_small_car #Hijo 2
                    
                    #Mutacion (hay que cambiarla para que se haga antes de crear los coches)
                    #Implementar la mutacion para individuos con codificacion real
                    

                    
                    for i in range(num_of_nnCars - 4):
                        #Nuevo individuo con codificación real
                        biases = np.random.randn(sum(sizes[1:]))
                        weights = np.random.randn(sum(y * x for x, y in zip(sizes[:-1], sizes[1:])))

                        genome = np.concatenate((biases, weights))

                        population.append(genome)
                        nnCars.append(Coche())


                    if number_track != 1:
                        for nncar in nnCars:
                            nncar.x = 140
                            nncar.y = 610 
                    
                    selectedCars.clear()

                    #print("Poblacion despues del cruce: ", len(nnCars), len(population))

            # Selección Manual
            # if event.key == ord ( "k" ):       # B: Nueva generacion
            #     if (len(selectedCars) == 2):
            #         for nncar in nnCars:
            #             nncar.score = 0
               
            #         alive = num_of_nnCars
            #         generation += 1
            #         selected = 0
            #         nnCars.clear() 
                    
            #         for i in range(num_of_nnCars):
            #             nnCars.append(Coche())
                        
            #         for i in range(0,num_of_nnCars-2,2):
            #             uniformCrossOverWeights(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
            #             uniformCrossOverBiases(selectedCars[0], selectedCars[1], nnCars[i], nnCars[i+1])
                    
            #         nnCars[num_of_nnCars-2] = selectedCars[0]
            #         nnCars[num_of_nnCars-1] = selectedCars[1]
                    
            #         nnCars[num_of_nnCars-2].car_image = green_small_car
            #         nnCars[num_of_nnCars-1].car_image = green_small_car
                    
            #         nnCars[num_of_nnCars-2].resetPosition()
            #         nnCars[num_of_nnCars-1].resetPosition()
                    
            #         nnCars[num_of_nnCars-2].collided = False
            #         nnCars[num_of_nnCars-1].collided = False
                                  
            #         for i in range(num_of_nnCars-2):
            #             for j in range(mutationRate):
            #                 mutateOneWeightGene(nnCars[i], auxcar)
            #                 mutateOneWeightGene(auxcar, nnCars[i])
            #                 mutateOneBiasesGene(nnCars[i], auxcar)
            #                 mutateOneBiasesGene(auxcar, nnCars[i])
            #         if number_track != 1:
            #             for nncar in nnCars:
            #                 nncar.x = 140
            #                 nncar.y = 610 
                      
            #         selectedCars.clear()
                    
            


            if event.key == ord ( "m" ):        # M: Nueva generacion y nuevo circuito
                if (len(selectedCars) == 2):
                    for nncar in nnCars:
                        nncar.score = 0
                   
                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    nnCars.clear() 
                    
                    for i in range(num_of_nnCars):
                        nnCars.append(Coche())
                        
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
                    nnCars.append(Coche())
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
            if mouses[0]: # Click izquierdo
                seleccion_manual_individuo()
    
            if mouses[2]:       # Click derecho
                eliminacion_manual_individuo()

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
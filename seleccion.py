# """Metodos de seleccion de individuos"""
# import pygame
# from vars import *
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon

# def seleccion_manual():

#         pos = pygame.mouse.get_pos()
#         point = Point(pos[0], pos[1])
#         #Revisar la lista de autos y ver cual estaba ahi
#         for nncar in nnCars:  
#             polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
#             if (polygon.contains(point)):
#                 if nncar in selectedCars:
#                     selectedCars.remove(nncar)
#                     selected -= 1
#                     if nncar.car_image == white_big_car:
#                         nncar.car_image = white_small_car 
#                     if nncar.car_image == green_big_car:
#                         nncar.car_image = green_small_car
#                     if nncar.collided:
#                         nncar.velocity = 0
#                         nncar.acceleration = 0
#                     nncar.update()
#                 else:
#                     if len(selectedCars) < 2:
#                         selectedCars.append(nncar)
#                         selected +=1
#                         if nncar.car_image == white_small_car:
#                             nncar.car_image = white_big_car  
#                         if nncar.car_image == green_small_car:
#                             nncar.car_image = green_big_car  
#                         if nncar.collided:
#                             nncar.velocity = 0
#                             nncar.acceleration = 0
#                         nncar.update()
#                 break
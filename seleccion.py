"""Modulo de operadores de seleccion de individuos"""

import pygame
from vars import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def seleccion_manual_individuo():
    """Seleccionar manualmente un individuo"""
    global selected
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
                if nncar.car_image == blue_big_car:
                    nncar.car_image = blue_small_car
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
                    if nncar.car_image == blue_small_car:
                        nncar.car_image = blue_big_car
                    if nncar.collided:
                        nncar.velocity = 0
                        nncar.acceleration = 0
                    nncar.update()
            break


def eliminacion_manual_individuo():
    """Eliminar manualmente un individuo"""
    global selected, alive
    pos = pygame.mouse.get_pos()
    point = Point(pos[0], pos[1])
    for nncar in nnCars:  
        polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
        if (polygon.contains(point)):
            if nncar not in selectedCars:
                nnCars.remove(nncar)
                alive -= 1
            break
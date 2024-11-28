"""Modulo para representar los textos en la interfaz grafica"""
from vars import *
def displayTexts():  
    global gameDisplay
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
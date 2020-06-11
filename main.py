import pygame
import random
import keyboard
import time

from chip8 import chip
#TODO make timer for controled clock, make system for passing keyboard input to class, make a draw flag


pygame.init()#should probably make this class inherit from the pygame class
screen = pygame.display.set_mode((640, 320))
screen.fill((46, 184, 46))
pygame.display.set_caption("CHIP-8 Emulator by Bailey Padovan")

pygame.display.set_icon(pygame.image.load('icon.png'))
b = pygame.Surface((640,320))#black object used to reset screen
b.fill((0,0,0))
pixel = pygame.image.load('pixel.png')



def update_display(object):
    temp = pygame.Surface((640,320))
    temp.blit(b,(0,0))
    i = 0
    while i < 2048:
        if object.display_buffer[i] == 1:
            x = i%64#how many between it and the side
            y = int(i/64)#how many between it and the top
            x = x*10
            y = y*10
            temp.blit(pixel,(x,y))

        i+=1
    screen.blit(temp,(0,0))
    object.draw = False
    pygame.display.update()



c = chip()
c.load_program("Breakout (Brix hack) [David Winter, 1997].ch8")#Maze (alt) [David Winter, 199x].ch8



update_display(c)


running = True
while running:
    print(time.perf_counter())
    c.clock_cycle()
    if c.draw == True:
        update_display(c)
    print(time.perf_counter())

    for event in pygame.event.get():#goes through events
        if event.type == pygame.QUIT:#must be capitals
             running = False

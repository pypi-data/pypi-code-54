#!/usr/bin/env python
"""
Porque cuando se dibuja un cuadrado sus esquinas no se pintan?
"""

#Import Modules
import pygame
from pygame.locals import *

import sys

pygame.init()
screen = pygame.display.set_mode((640,480))

screen.fill((255,255,255))

rect = Rect(150,50,320,320)
pygame.draw.rect(screen, (0,0,0), rect, 30)


pygame.display.flip()



clock = pygame.time.Clock()
while True:
    clock.tick(10) #slower than 10 frame per second
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)

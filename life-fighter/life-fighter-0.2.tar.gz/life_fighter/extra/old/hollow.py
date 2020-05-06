# Hollow/Outline text module 
# based on code by: Pete Shinners
# http://www.pygame.org/pcr/hollow_outline/index.php

"""
two text rendering styles. outlined and hollow. both
use a single pixel border around the text. you might be
able to cheat a bigger border by fooling with it some.
"""
import os, sys, pygame, pygame.font, pygame.image
from pygame.locals import *

def textOutline(font, message, fontcolor, outlinecolor):
    borde = font.render(message, 1, outlinecolor)
    base = font.render(message, 1, fontcolor)
    img = pygame.Surface( base.get_rect().inflate(2,2).size, 0, base )
    for x in 0,2:
        for y in 0,2:
            img.blit(borde, (x,y) )
    img.blit(base, (1, 1))
    return img

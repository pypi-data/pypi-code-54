#!/usr/bin/env python
"""
This file is part of Life Fighter.
"""

#Import Modules
import pygame
from pygame.locals import *
from sprites import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#Defined values
WINDOW_TITLE = "Life Fighter 0.01"
width = 800
height = 600
#n = 10
n1 = 18
n2 = 14
#if n < 20:
#    line = 2
#else:
#    line = 1
line = 1
x_off = 25
y_off = 75
#step = (width - 2 * x_off) / n1
#step = (height - 2 * y_off) / n2
step = 35

def main():
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bg_color)

#Display The Background
    screen.blit(background, (0, 0))
    #pygame.display.flip()

    grid = Grid(n1, n2, x_off, y_off, step, line)
    #gridGroup = pygame.sprite.RenderUpdates()#no pude user GroupSingle :(
    #gridGroup.add(grid)
    cellsGroup = pygame.sprite.RenderUpdates()
    #Test
    glider = [(1,0), (2,1), (0,2), (1,2), (2,2)]
    other = [(5,5), (5,6), (5,7)]
    for key in glider + other:
        grid.cells[key].birth_now()
        #cellsGroup.add(grid.cells[key])

    grid.set_hero(2,1)

    #ENT Test
    
    for key in grid.cells:
       cellsGroup.add(grid.cells[key])

    #gridGroup.draw(screen)
    screen.blit(grid.image, grid.rect)
    cellsGroup.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()
    

#Main loop
    while True:

        clock.tick(10) #slower than 10 frame per second

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    grid.beat()
                elif event.key == K_LEFT:
                    grid.hero_left()
                elif event.key == K_RIGHT:
                    grid.hero_right()
                elif event.key == K_UP:
                    grid.hero_up()
                elif event.key == K_DOWN:
                    grid.hero_down()

                screen.blit(grid.image, grid.rect)
                #cellsGroup.empty()
                #cellsGroup.add(alive_cells)
                cellsGroup.draw(screen)
                pygame.display.flip()
                #pygame.display.update(rects)



if __name__ == '__main__':
    main()

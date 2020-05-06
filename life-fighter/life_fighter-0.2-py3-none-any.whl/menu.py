# The Menu class was originally develop by Juanjo Conti <jjconti@gmail.com>
# for Life Fighter game. It is intentionally placed in a separeted file so you
# can use it if it's fine for you. If not you can improve it :-)
# Please use it under GPL licence like the rest of the game.

# I'm sorry. I have no include exausted controls here, so be carefull with the size
# of the images you use.

import sys

import pygame
from pygame.locals import *

class Menu(object):
    '''A generic menu user interface. Allow both keyboard and mouse selection'''

    def __init__(self, screen, background, font1, font2, font_title, color1, color2, \
                 tit_color, snd1, snd2, title, options, index=0):
        '''font1 will be used for the selected item and font2 for unselected ones,
           sound1 will be used while switching items and sound2 when one is selected '''
        self.screen = screen
        self.items = [x[0] for x in options]
        self.returns = [x[1] for x in options]
        #self.n_items = len(items)
        self.last_index = len(self.items) - 1
        self.index = index
        self.done = False
        self.hor_step = max(font1.get_height(), font2.get_height())
        self.clock = pygame.time.Clock()
        self.selected_imgs = [font1.render(text, True, color1) for text in self.items]
        self.unselected_imgs = [font2.render(text, True, color2) for text in self.items]
        self.unselected_rects = None
        self.sounds = {}
        self.sounds["snd1"] = snd1
        self.sounds["snd2"] = snd2
        
        #self.screen.blit(self.background, (0,0))
        title_img = font_title.render(title, True, tit_color)
        topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        bg = background.copy()
        bg.blit(title_img, topleft)
        self.background = bg


        self._draw_items()

        #pygame.mouse.set_pos(self.unselected_rects[index].center)
        
        #pygame.display.flip()

    def main_loop(self):
        '''Returns the asosiated object for the selected item'''

        while not self.done:

            self.clock.tick(10)

            self.screen.blit(self.background, (0,0))    

            for event in pygame.event.get():
                self.control(event)

            self._draw_items()

            pygame.display.flip()
            
        return self.returns[self.index]

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_SPACE, K_RETURN, K_KP_ENTER):
                self.select()
            elif event.key == K_UP:
                if self.index > 0:
                    self.set_index(self.index - 1)
                else:
                    self.set_index(self.last_index)
            elif event.key == K_DOWN:
                if self.index < self.last_index:
                    self.set_index(self.index + 1)
                else:
                    self.set_index(0)
            #elif event.key == K_ESCAPE:
            #    '''Do you think this feature is good?'''
            #    self.index = self.last_index
            #    self.select()
        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            for i in range(len(self.unselected_rects)):
                r = self.unselected_rects[i]
                if r.collidepoint(x,y):
                    self.set_index(i)
                    return
        if event.type == MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for i in range(len(self.unselected_rects)):
                r = self.unselected_rects[i]
                if r.collidepoint(x,y):
                    self.select()
                    return
                
    def set_index(self, index):
        if self.index != index:
            self.sounds["snd1"].play()
            self.index = index

    def select(self):
        self.sounds["snd2"].play()
        self.done = True

    def _draw_items(self):
        rects = []
        y = self.hor_step + 100 # Tune this value as you need
        for i in range(len(self.items)):
            if i == self.index:
                img = self.selected_imgs[i]
            else:
                img = self.unselected_imgs[i]
            x = (self.screen.get_width() - img.get_width()) / 2
            self.screen.blit(img, (x,y))
            
            if self.unselected_rects is None:
                rects += [img.get_rect().move(x,y)]

            y += self.hor_step

        if self.unselected_rects is None:
            self.unselected_rects = rects

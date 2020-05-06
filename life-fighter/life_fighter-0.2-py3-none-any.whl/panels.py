# The TextPanel class was originally develop by Juanjo Conti <jjconti@gmail.com>
# for Life Fighter game. It is intentionally placed in a separeted file so you
# can use it if it's fine for you. If not you can improve it :-)
# Please use it under GPL licence like the rest of the game.

# I'm sorry. I have no include exausted controls here, so be carefull with the size
# of the images you use.

import sys

import pygame
from pygame.locals import *

class TextPanel(object):
    '''A generic TextPanel for showing text information.'''

    def __init__(self, hd, title, lines, f_father):
        '''hd.font1 will be used for the title and hd.font2 for the text in lines:
        ["this is text for one line", "this for a second one", .. ]'''
        self.screen = hd.screen
        self.done = False
        self.font = hd.font2
        self.color = hd.color2
        self.lines = lines
        self.hor_step = hd.font2.get_height()
        self.clock = pygame.time.Clock()
        self.f_father = f_father
        
        #self.screen.blit(self.background, (0,0))
        title_img = hd.font1.render(title, True, hd.color1)
        topleft = (hd.bg.get_rect().width - title_img.get_rect().width) / 2, 30
        bg = hd.bg.copy()
        bg.blit(title_img, topleft)
        self.background = bg

    def main_loop(self):

        while not self.done:

            self.clock.tick(10)

            self.screen.blit(self.background, (0,0))    

            for event in pygame.event.get():
                self.control(event)

            self._draw_lines()
            pygame.display.flip()

        return self.f_father
            

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_SPACE, K_RETURN, K_KP_ENTER, K_DOWN):
                self.next()
            elif event.key in (K_UP, K_BACKSPACE):
                self.prev()
            elif event.key == K_ESCAPE:
                self.back()
        if event.type == MOUSEBUTTONDOWN:
            self.next()

    def _draw_lines(self):
        y = self.hor_step + 100 # Tune this value as you need
        for line in self.lines:
            line_img = self.font.render(line, True,self.color)
            x = (self.screen.get_width() - line_img.get_width()) / 2
            self.screen.blit(line_img, (x,y))
            
            y += self.hor_step

    def next(self):
        pass

    def prev(self):
        pass

    def back(self):
        self.done = True

CURSOR = '|'

class InputPanel(object):
    '''A generic input panel.'''

    def __init__(self, screen, background, font1, font2, color1, color2, \
                 snd1, snd2, title):
        '''font1 and color1 will be used for the title and font2 and color2 for the
           input text. '''
        self.cursor = CURSOR
        self.text = ""
        self.screen = screen
        self.font = font2
        self.color = color2
        self.done = False
        self.clock = pygame.time.Clock()
        self.sounds = {}
        self.sounds["snd1"] = snd1
        self.sounds["snd2"] = snd2
        
        title_img = font1.render(title, True, color1)
        topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        bg = background.copy()
        bg.blit(title_img, topleft)
        self.background = bg


        self._draw_text()

    def main_loop(self):
        '''Returns the asosiated object for the selected item'''

        while not self.done:

            self.clock.tick(10)

            self.screen.blit(self.background, (0,0))    

            for event in pygame.event.get():
                self.control(event)
                
            self._draw_text()

            pygame.display.flip()
            
        return self.text

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_RETURN, K_KP_ENTER):
                self.enter()
            else:
                char = event.unicode
                if self.valid_char(char):
                    self.text += char
                    self.sounds["snd1"].play()
                    self._draw_text()
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.sounds["snd1"].play()
                    self._draw_text()

    def valid_char(self, char):
        if char:
            if char in u" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUVWXYZ1234567890":
                return True
        return False
               
    def enter(self):
        self.sounds["snd2"].play()
        self.done = True

    def _draw_text(self):
        y = 250 # Tune this value as you need
        text_img = self.font.render(self.text + self.cursor, True, self.color)
        x = (self.screen.get_width() - text_img.get_width()) / 2
        self.screen.blit(text_img, (x,y))

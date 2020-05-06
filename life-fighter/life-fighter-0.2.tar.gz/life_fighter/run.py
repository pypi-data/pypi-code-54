#!/usr/bin/env python
'''
Starts Life Fighter.
'''

#Import Modules
import pygame
from pygame.locals import *

from settings import *
from help_text import *
from utils import *
from life import Grid
from stages import *
from menu import Menu
from panels import TextPanel
from highscores import hof

import sys

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def main():
    #Initialize 
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    icon = load_image(ICON)
    pygame.display.set_icon(icon)

    background = load_image(BGIMAGE1)
    screen.blit(background, (0, 0))

    #Create the game clock
    clock = pygame.time.Clock()

    #Menus data
    font0 = pygame.font.Font(FONT1, 65)
    font1 = pygame.font.Font(FONT1, 50)
    font2 = pygame.font.Font(FONT1, 45)
    font3 = pygame.font.Font(FONT1, 40)
    font4 = pygame.font.Font(FONT1, 35)
    font5 = pygame.font.Font(FONT1, 25)
    sound1 = load_sound(TYPEW1)
    sound2 = load_sound(TYPEW2)

    #Package stages data
    sd = DataBag()
    sd.clock = clock
    sd.screen = screen
    sd.bg = background
    sd.grid = Grid(n1, n2, x_off, y_off, step, line)

    #Package help data
    hd = DataBag()
    hd.screen = screen
    hd.bg = background
    hd.font1 = font1
    hd.font2 = font5
    hd.color1 = color1
    hd.color2 = color5

    #Menu functions

    def f_exit():
        sys.exit(0)

    def f_train():
        return Train(sd, True, f_play)

    def f_moves():
        return Moves(sd, False, f_play)

    def f_clock():
        return Clock(sd, False, f_play)

    def f_life():
        return Life(sd, f_main)

    def f_editor():
        return Editor(sd, f_main)

    def f_play():
        options = [("Entrenamiento", f_train),
                   ("Cuenta pasos", f_moves),
                   ("Contrarreloj", f_clock),
                   ("Combinado", None),
                   ("Volver", f_main),]
        
        return Menu(screen, background, font1, font2, font0, color1, color2, color5, \
                    sound1, sound2, "Jugar", options)

    def f_scores():
        return TextPanel(hd, "Salón de la fama", hof.score_lines(), f_main)

    def f_hgame():
        return TextPanel(hd, "El Juego", the_game, f_help)

    def f_hrules():
        return TextPanel(hd, "Las reglas", the_rules, f_help)

    def f_hcontrols():
        return TextPanel(hd, "Controles", controls, f_help)

    def f_hcredits():
        return TextPanel(hd, "Créditos", the_credits, f_help)

    def f_help():
        options = [("El juego", f_hgame),
                   ("Reglas de evolución", f_hrules),
                   ("Controles", f_hcontrols),
                   ("Créditos", f_hcredits),
                   ("Volver", f_main),]
        
        return Menu(screen, background, font1, font2, font0, color1, color2, color5, \
                sound1, sound2, "Ayuda", options)

    def f_main():
        options = [("Jugar", f_play),
                   ("Salon de la fama", f_scores),
                   ("Vida", f_life),
                   ("Editor", f_editor),
                   ("Configuración", None),
                   ("Ayuda", f_help),
                   ("Salir", f_exit),]
        
        return Menu(screen, background, font3, font4, font0, color1, color2, color5, \
                sound1, sound2, WINDOW_TITLE, options)


    f = f_main

    while f is not f_exit:
        op = f().main_loop()
        if op:
            f = op

    f()


if __name__ == '__main__':
    main()

from pygame.locals import USEREVENT

WINDOW_TITLE = "Life Fighter 0.2"
width = 800
height = 600

n1 = 18 * 2
n2 = 14 * 2
step = 35 // 2
#n1 = 18
#n2 = 14
#step = 35
line = 1
x_off = 25
y_off = 75

#Stages

TRAIN_TITLE = "Entrenamiento"
MOVES_TITLE = "Cuenta pasos"
CLOCK_TITLE = "Contrarreloj"
EDITOR_TITLE = "Editor"
LIFE_TITLE = "Juego de la Vida de Conway"

SECOND = 1000 # in milliseconds
TIMEEVENT = USEREVENT + 1

#Colours

grid_color = (0,0,0)
cell_color = (0,0,0)
hero_color = (0,0,200)
dead_color = (200, 0, 0)
bg_color = (250, 250, 250)
bg_color_game = (0, 5, 5)
#score_color = (255, 0, 0)
#time_color = (255, 0, 45)
#steps_color = (133, 189, 103)
#title_color = (250, 150, 150)
color1 = (0, 5, 5)
color2 = (240, 240, 240)
#color3 = (0, 0, 200)
#color4 = (20, 20, 100)
color5 = (155, 16, 16)
score_color = time_color = steps_color = title_color = color3 = color4 = color5
paper_color = (255, 250, 215)

black = (0,0,0)
white = (255, 255, 255)


#Files

import os

DATA = os.path.join("life_fighter", "data")
HIGHSCORES = os.path.join(DATA, "scores.high")
IMGS = os.path.join(DATA, "imgs")
BACKGROUNDS = os.path.join(IMGS, "backgrounds")
SOUNDS = os.path.join(DATA, "sounds")
MUSIC = os.path.join(DATA, "music")
FONTS = os.path.join(DATA, "fonts")
CELLS = os.path.join(DATA, "cells")
GAME_CELLS = os.path.join(CELLS, "games")
CONWAY_CELLS = os.path.join(CELLS, "conway")

ICON = os.path.join(IMGS, "life_icon.png")
#BGIMAGE1 = os.path.join(BACKGROUNDS, "paper3.png")
BGIMAGE1 = os.path.join(BACKGROUNDS, "white.png")
PLAY = os.path.join(IMGS, "play.png")
STOP = os.path.join(IMGS, "stop.png")
NEXT = os.path.join(IMGS, "next.png")
PREV = os.path.join(IMGS, "prev.png")

BLOOP = os.path.join(SOUNDS, "bloop.wav")
TYPEW1 = os.path.join(SOUNDS, "9744_Horn_typewriter-shorter.wav")
TYPEW2 = os.path.join(SOUNDS, "9098_ddohler_Typewriter.wav")

                      
FONT1 = os.path.join(FONTS,"FreeMonoBold.ttf")
#FONT1 = os.path.join(FONTS,"ds_moster.ttf")
#FONT2 = os.path.join(FONTS, "FreeSerifBold.ttf")
#FONT1 = None
import os, sys, random, pickle

import pygame
from pygame.locals import *
from pygame.time import set_timer

from settings import *
from utils import *
from life import Pattern
from menu import Menu
from panels import InputPanel
from highscores import hof

class Stage(object):
    '''A stage is what you see at the screen while playing.'''
    def __init__(self, sd, f_father):
        self.clock = sd.clock
        self.screen = sd.screen
        self.background = sd.bg.copy()
        self.grid = sd.grid
        self.f_father = f_father
        self.cells_group = pygame.sprite.RenderUpdates()
        self.cells_group.add(self.grid.cells.values())
        self.redraw_group = pygame.sprite.RenderUpdates()

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self._beat()
            if event.key == K_ESCAPE:
                self._quit()

    def _beat(self, dead_alert=False):
        self.grid.beat(dead_alert)

class Game(Stage):
    '''An abstract game.'''

    def __init__(self, sd, dead_alert, f_father):
        Stage.__init__(self, sd, f_father)
        self.level = 0
        self.points = 0
        self.playing = True
        self.coin_value = 1
        self.dead_alert = dead_alert
        self.name = self._load_cells()
        self.hero_start_pos = self.grid.get_hero()
        self._add_labels()
        self.redraw_group.add(self.score)

    def control(self, event):
        Stage.control(self, event)
        grid = self.grid
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                grid.hero_left(self.dead_alert)
            elif event.key == K_RIGHT:
                grid.hero_right(self.dead_alert)
            elif event.key == K_UP:
                grid.hero_up(self.dead_alert)
            elif event.key == K_DOWN:
                 grid.hero_down(self.dead_alert)
            elif event.key == K_n:
                self.next_level()
            elif event.key == K_s:
                print("on/off sounds")
            elif event.key == K_m:
                print("on/off music")
            elif event.key == K_p:
                print("pause game")
                
    def main_loop(self):
        
        while self.playing:

            self.clock.tick(10) #slower than 10 frame per second

            for event in pygame.event.get():
                self.control(event)

            self.screen.blit(self.background, (0,0))    
            self.screen.blit(self.grid.image, self.grid.rect)
            self.cells_group.draw(self.screen)
            self.update_sprites()
            self.redraw_group.draw(self.screen)
            pygame.display.flip() # USE UPDATE

            if not self.grid.is_hero_alive():
                self.finish_game()

        return self.f_father

    def _quit(self):
        self.playing = False

    def update_sprites(self):
        self.score.update(self.points)
        
    def _load_cells(self):
        '''Randomly load a previusly persisted cells poblation.'''

        self.grid.kill_all()
        
        pobs = [p for p in os.listdir(GAME_CELLS) if p.endswith(".pob")]
        name = random.choice(pobs)
        pob = pickle.load(open(os.path.join(GAME_CELLS, name), 'rb'))
        self.grid.add_living_cells(pob)
        i,j = random.choice(pob)
        self.grid.set_hero(i, j, self.dead_alert)

        return name[0].upper() + name[1:-4].lower()

    def _beat(self):
        Stage._beat(self, self.dead_alert)
        if self.grid.is_hero_alive() and not self.same_place():
            self.update_points()
            self.hero_start_pos = self.grid.get_hero()

    def same_place(self):
        '''Did the hero chang its position since last beat?'''
        return self.hero_start_pos == self.grid.get_hero()
            
    def _add_labels(self):
        
        text = self.title + ": " + self.name
        font = pygame.font.Font(FONT1, 40)
        w,h = font.size(text)
        x = x_off + (n1 * step - w) // 2
        y = (y_off - h) // 2
        img = font.render(text, True, title_color)
        self.background.blit(img, (x,y))

        text = "Score"
        font = pygame.font.Font(FONT1, 30)
        w,h = font.size(text)
        a = x_off + step * n1
        x = a + (width - a - w) // 2 
        y = y_off
        img = font.render(text, True, score_color)
        self.background.blit(img, (x,y))

        self.score = Score(w, x, y + h)

        self._add_specific_labels()

    def _add_specific_labels(self):
        pass

    def update_points(self):
        self.points += self.coin_value
        print(self.points)

    def next_level(self):
        self.level += 1
        self.coin_value *= 2

    def finish_game(self):
        '''Before exiting, we ask if the player want to play again'''

        self.high_scores()

        def true():
            return True

        def false():
            return False

        def maybe():
            return random.choice((True, False, True))

        def m_not():
            return random.choice((False, True, False))

        def you():
            return random.choice((True, False))   

        options = [("¡Si!", true),
                   ("No...", false),
                   ("Tal vez", maybe),
                   ("Creo que no", m_not),
                   ("Decidí vos", you),]

        font0 = pygame.font.Font(FONT1, 65)
        font1 = pygame.font.Font(FONT1, 50)
        font2 = pygame.font.Font(FONT1, 45)
        sound1 = load_sound(TYPEW1)
        sound2 = load_sound(TYPEW2)

        bg = load_image(BGIMAGE1)
        
        f = Menu(self.screen, bg, font1, font2, font0, color1, color2, color5, \
                sound1, sound2, "¿Jugar otra vez?", options).main_loop()

        if f():        
            self.name = self._load_cells()
            self.hero_start_pos = self.grid.get_hero()
        else:
            self.playing = False

    def high_scores(self):
        if self.points > hof.minor_value():

            font1 = pygame.font.Font(FONT1, 50)
            font2 = pygame.font.Font(FONT1, 45)
            sound1 = load_sound(TYPEW1)
            sound2 = load_sound(TYPEW2)
            bg = load_image(BGIMAGE1)
            
            name = InputPanel(self.screen, bg, font1, font2, \
                              color1, color5, sound2, sound2, "Ingrese su nombre:").main_loop()
            
            hof.add(name, self.points)
        
            
                        
class Train(Game):
    '''A game for training yourself.'''

    def __init__(self, sd, dead_alert, f_father):
        self.title = TRAIN_TITLE
        Game.__init__(self, sd, dead_alert, f_father)
        
    def control(self, event):
        Game.control(self, event)

    def next_level(self):
        Game.next_level(self)
        self._beat()
        	

class Moves(Game):
    '''A game where moves count.'''

    def __init__(self, sd, dead_alert, f_father):
        self.title = MOVES_TITLE
        Game.__init__(self, sd, dead_alert, f_father)
        self.max_moves = 10
        self.moves = self.max_moves
        self.redraw_group.add(self.stepCounter)

    def control(self, event):
        i,j = self.grid.get_hero()
        Game.control(self, event)
        if (i,j) != self.grid.get_hero():
            self.moves -= 1
            if self.moves == 0:
                self._beat()

    def update_sprites(self):
        Game.update_sprites(self)
        self.stepCounter.update(self.moves)

    def _beat(self):
        Game._beat(self)
        self.moves = self.max_moves

    def _add_specific_labels(self):
        text = "Moves"
        font = pygame.font.Font(FONT1, 30)
        w,h = font.size(text)
        a = x_off + step * n1
        x = a + (width - a - w) // 2 
        y = y_off + 100
        img = font.render(text, True, score_color)
        #img = textOutline(font, text, score_color, black)
        self.background.blit(img, (x,y))

        self.stepCounter = StepCounter(w, x, y + h, 10)

    def next_level(self):
        if not self.last_level():
            Game.next_level(self)
            self.max_moves -= 1
            self._beat()

    def last_level(self):
        return self.max_moves == 1

       
class Clock(Game):
    '''A game where time matters.'''

    def __init__(self, sd, dead_alert, f_father):
        self.title = CLOCK_TITLE
        Game.__init__(self, sd, dead_alert, f_father)
        self.max_time = 10 * SECOND 
        self.time = self.max_time
        self.redraw_group.add(self.timer)
        set_timer(TIMEEVENT, SECOND)

    def control(self, event):
        Game.control(self, event)
        if event.type == TIMEEVENT:
            self.time -= SECOND
            if self.time == 0:
                self._beat()

    def update_sprites(self):
        Game.update_sprites(self)
        self.timer.update(self.time // SECOND)
        

    def _beat(self):
        Game._beat(self)
        self.time = self.max_time
        set_timer(TIMEEVENT, 0)
        set_timer(TIMEEVENT, SECOND)

    def _add_specific_labels(self):
        text = "Time"
        font = pygame.font.Font(FONT1, 30)
        w,h = font.size(text)
        a = x_off + step * n1
        x = a + (width - a - w) // 2 
        y = y_off + 100
        img = font.render(text, True, score_color)
        self.background.blit(img, (x,y))

        self.timer = Timer(w, x, y + h, 10)

    def next_level(self):
        if not self.last_level():
            Game.next_level(self)
            self.max_time -= SECOND
            self._beat()

    def last_level(self):
        return self.max_time == SECOND
        

class Score(pygame.sprite.Sprite):
    '''Points displayed at the screen.'''

    def __init__(self, w, x, y, default = 0):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(FONT1, 25)
        
        self.image = self.font.render(str(default), True, score_color)
        self.w = w
        self.x = x
        self.y = y
        x += (w - self.image.get_width()) // 2

        self.rect = self.image.get_rect(topleft=(x,y))
        
    def update(self, points):
        self.image = self.font.render(str(points), True, score_color)
        x = self.x + (self.w - self.image.get_width()) // 2
        self.rect = self.image.get_rect(topleft=(x,self.y))

class Timer(pygame.sprite.Sprite):
    '''Display at the screen your time at the Clock game.'''

    def __init__(self, w, x, y, default):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(FONT1, 25)
        
        self.image = self.font.render(str(default), True, time_color)
        self.w = w
        self.x = x
        self.y = y
        x += (w - self.image.get_width()) // 2

        self.rect = self.image.get_rect(topleft=(x,y))
        
    def update(self, seconds):
        self.image = self.font.render(str(seconds), True, time_color)
        x = self.x + (self.w - self.image.get_width()) // 2
        self.rect = self.image.get_rect(topleft=(x,self.y))

class StepCounter(pygame.sprite.Sprite):
    '''Display at the screen your avaliable moves at Moves game.'''

    def __init__(self, w, x, y, default):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(FONT1, 25)
        
        self.image = self.font.render(str(default), True, steps_color)
        self.w = w
        self.x = x
        self.y = y
        x += (w - self.image.get_width()) // 2

        self.rect = self.image.get_rect(topleft=(x,y))
        
    def update(self, seconds):
        self.image = self.font.render(str(seconds), True, steps_color)
        x = self.x + (self.w - self.image.get_width()) // 2
        self.rect = self.image.get_rect(topleft=(x,self.y))


        
class Editor(Stage):
    '''A life editor.'''

    def __init__(self, sd, f_father):
        Stage.__init__(self, sd, f_father)
        self.sounds = {}
        self.sounds["bloop"] = load_sound(BLOOP)
        self._add_labels()
        self.redraw_group.add(self.alive_cells)
        self.done = False

    def _add_labels(self):
        text = EDITOR_TITLE
        font = pygame.font.Font(FONT1, 40)
        w,h = font.size(text)
        x = x_off + (n1 * step - w) // 2
        y = (y_off - h) // 2
        img = font.render(text, True, title_color)
        self.background.blit(img, (x,y))

        text = "Vivas"
        font = pygame.font.Font(FONT1, 30)
        w,h = font.size(text)
        a = x_off + step * n1
        x = a + (width - a - w) // 2 
        y = y_off + 100
        img = font.render(text, True, score_color)
        self.background.blit(img, (x,y))

        self.alive_cells = AliveCells(w, x, y + h, 0)

    def update_sprites(self):
        self.alive_cells.update(self.grid.alive_cells())

    def main_loop(self):
        while not self.done:

            self.clock.tick(10) #slower than 10 frame per second

            for event in pygame.event.get():
                self.control(event)

            self.screen.blit(self.background, (0,0))    
            self.screen.blit(self.grid.image, self.grid.rect)
            self.cells_group.draw(self.screen)
            self.update_sprites()
            self.redraw_group.draw(self.screen)
            pygame.display.flip() # USE UPDATE

        return self.f_father

    def _quit(self):
        self.done = True

    def control(self, event):
        Stage.control(self, event)

        if event.type == KEYDOWN:
            if event.key in (K_g, K_c):
                self._persist_cells(event.key)

        elif event.type == MOUSEBUTTONDOWN:
            i,j =  event.pos
            i -= x_off
            i //= step
            j -= y_off
            j //= step
            
            if -1 < i < n1 and -1 < j < n2:
                if event.button == 1:
                    self.grid.cells[i,j].birth_now()
                    self.sounds["bloop"].play()
                elif event.button == 3:
                    self.grid.cells[i,j].die_now()
                    self.sounds["bloop"].play()
                    
    def _persist_cells(self, key):
        
        if key == K_c:
            name = input("Insert a name (Conway): ")
            kind = input("Insert a kind: ")
            period= input("Insert a period (if apply): ")
            cells = [k for k in self.grid.cells if self.grid.cells[k].is_alive()]
            o = Pattern(name, kind, period, cells)
            file_name = os.path.join(CONWAY_CELLS, name + ".pat")
        elif key == K_g:
            name = input("Insert a name (game): ")
            o = [k for k in self.grid.cells if self.grid.cells[k].is_alive()]
            file_name = os.path.join(GAME_CELLS, name + ".pob")
            
        f = open(file_name, 'wb')
        pickle.dump(o, f)
        f.close()

       
class Life(Stage):
    '''Conway\'s Game of Life with lots of patterns.'''

    def __init__(self, sd, f_father):
        Stage.__init__(self, sd, f_father)
        self.patterns = Circular(self._load_patterns())
        self._load_cells(self.patterns[0])
        self.play_img = load_image(PLAY)
        self.stop_img = load_image(STOP)
        self.prev_img = load_image(PREV)
        self.next_img = load_image(NEXT)
        self._add_labels()
        self.redraw_group.add(self.alive_cells)
        self.done = False

    def _load_patterns(self):
        '''Return a list of persisted life patterns.'''

        pat_files = [p for p in os.listdir(CONWAY_CELLS) if p.endswith(".pat")]
        patterns = [pickle.load(open(os.path.join(CONWAY_CELLS, p), 'rb')) for p in pat_files]
        return patterns

    def _load_cells(self, pat):
        self.grid.kill_all()
        pob = pat.alive_cells
        self.grid.add_living_cells(pob)

    def _add_labels(self):
        text = LIFE_TITLE
        font = pygame.font.Font(FONT1, 40)
        w,h = font.size(text)
        x = x_off + (n1 * step - w) // 2
        y = (y_off - h) // 2
        img = font.render(text, True, title_color)
        self.background.blit(img, (x,y))

        text = "Vivas"
        font = pygame.font.Font(FONT1, 30)
        w,h = font.size(text)
        a = x_off + step * n1
        x = a + (width - a - w) // 2 
        y = y_off + 100
        img = font.render(text, True, color4)
        self.background.blit(img, (x,y))

        self.alive_cells = AliveCells(w, x, y + h, 0)

        y += 2 * h
        bw = self.play_img.get_rect().width
        x = x + (w - 2 * bw) // 2
        self.play_rect = self.play_img.get_rect().move(x,y)
        self.stop_rect = self.stop_img.get_rect().move(x+bw,y)
        y += self.play_img.get_rect().height
        self.prev_rect = self.prev_img.get_rect().move(x,y)
        self.next_rect = self.next_img.get_rect().move(x+bw,y)

        self.background.blit(self.play_img, self.play_rect)
        self.background.blit(self.stop_img, self.stop_rect)
        self.background.blit(self.prev_img, self.prev_rect)
        self.background.blit(self.next_img, self.next_rect) 


    def update_sprites(self):
        self.alive_cells.update(self.grid.alive_cells())

    def main_loop(self):
        while not self.done:

            self.clock.tick(10) #slower than 10 frame per second

            for event in pygame.event.get():
                self.control(event)

            self.screen.blit(self.background, (0,0))    
            self.screen.blit(self.grid.image, self.grid.rect)
            self.cells_group.draw(self.screen)
            self.update_sprites()
            self.redraw_group.draw(self.screen)
            pygame.display.flip() # USE UPDATE

        return self.f_father

    def _quit(self):
        self.done = True

    def control(self, event):
        Stage.control(self, event)

        if event.type == MOUSEBUTTONDOWN:
            i,j = event.pos
            if self.play_rect.collidepoint(i,j):
                self.play()
            elif self.stop_rect.collidepoint(i,j):
                self.stop()
            elif self.prev_rect.collidepoint(i,j):
                self.prev()
            elif self.next_rect.collidepoint(i,j):
                self.next()
        if event.type == TIMEEVENT:
            self._beat()

    def play(self):
        set_timer(TIMEEVENT, SECOND//2)

    def stop(self):
        set_timer(TIMEEVENT, 0)

    def prev(self):
        pat = self.patterns.prev()
        self._load_cells(pat)

    def next(self):
        pat = self.patterns.next()
        self._load_cells(pat)

class AliveCells(pygame.sprite.Sprite):
    '''Number of alive cells in the grid.'''

    def __init__(self, w, x, y, default = 0):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(FONT1, 25)
        
        self.image = self.font.render(str(default), True, color3)
        self.w = w
        self.x = x
        self.y = y
        x += (w - self.image.get_width()) // 2

        self.rect = self.image.get_rect(topleft=(x,y))
        
    def update(self, cells):
        self.image = self.font.render(str(cells), True, color3)
        x = self.x + (self.w - self.image.get_width()) // 2
        self.rect = self.image.get_rect(topleft=(x,self.y))
            
class Generation(pygame.sprite.Sprite):
    '''Number of the current generation.'''

    def __init__(self, w, x, y, default = 0):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(FONT1, 25)
        
        self.image = self.font.render(str(default), True, color3)
        self.w = w
        self.x = x
        self.y = y
        x += (w - self.image.get_width()) // 2

        self.rect = self.image.get_rect(topleft=(x,y))
        
    def update(self, generation):
        self.image = self.font.render(str(generation), True, color3)
        x = self.x + (self.w - self.image.get_width()) // 2
        self.rect = self.image.get_rect(topleft=(x,self.y))

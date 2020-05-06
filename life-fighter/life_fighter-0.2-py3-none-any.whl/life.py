import os

import pygame
from pygame.locals import *

from settings import *

DEAD = 0
ALIVE = 1


class Cell(pygame.sprite.Sprite):
    '''A life cell'''
    
    def __init__(self, grid, state, x_off, y_off, i, j):        
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self.next_state = state
        self.grid = grid
        self.color = cell_color
        step = self.grid.step
        self._image()
        self.rect = self.image.get_rect()      
        self.rect.x = x_off + i * step
        self.rect.y = y_off + j * step

    def __str__(self):
        return str(self.state)
		
    def get_state(self):
        return self.state

    def is_alive(self):
        return self.state == ALIVE
	    
    def set_next_state(self, state):
        self.next_state = state

    def birth(self):
        self.set_next_state(ALIVE)

    def birth_now(self):
        self.state = ALIVE
        self.next_state = ALIVE
        self._image()

    def die(self):
        self.set_next_state(DEAD)

    def die_now(self):
        self.state = DEAD
        self.next_state = DEAD
        # Make sure no cell remember the hero color
        self.color = cell_color
        self._image()
		
    def update_state(self):
        self.state = self.next_state
        self._image()
        
    def _image(self):
        step = self.grid.step
        self.image = pygame.Surface((step, step))
        self.image.set_colorkey(bg_color)
        self.image.fill(bg_color)
        if self.is_alive():
            pos = (step // 2 + 1, step // 2 + 1)
            radius = int(0.4 * step)
            pygame.draw.circle(self.image, self.color, pos, radius, 0)
            self.image.set_alpha(150)

    def be_hero(self, color):
        self.color = color
        self.birth_now()

    def be_normal(self):
        self.color = cell_color
        self.die_now()


class Grid(pygame.sprite.Sprite):
    '''A life grid'''

    def __init__(self, columns, rows, x_off, y_off, step, line):
        pygame.sprite.Sprite.__init__(self)
        self.columns = columns
        self.rows = rows
        self.step = step
        self.cells = {}

        for i in range(columns):
            for j in range(rows):
                self.cells[i,j] = Cell(self, DEAD, x_off, y_off, i, j)

        self.hero_alive = False

        self.rect = Rect(x_off, y_off, step * columns, step * rows)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.set_colorkey(bg_color)
        self.image.fill(bg_color)
        r = Rect(0, 0, step * columns, step * rows)
        pygame.draw.rect(self.image, grid_color, r, line)

        for i in range(step, step * columns, step):
            start = (i, line)
            end = (i, step * rows +line - 1)
            pygame.draw.line(self.image, grid_color, start, end, line)

        for i in range(step, step * rows, step):
            start = (line, i)
            end = (step * columns + line - 1, i)
            pygame.draw.line(self.image, grid_color, start, end, line)

    def __str__(self):
        s = ""
        for j in range(self.rows):
            for i in range(self.columns):
                s += str(self.cells[i,j])
            s += "\n"
        return s
				
    def add_cells(self, cells):
        '''cells is a dict of Cells'''
        for k in cells:
            self.cells[k] = cells[k]

    def add_living_cells(self, cells):
        '''cells is a list of tuples i,j'''
        for k in cells:
            self.cells[k].birth_now()

    def alive_neights(self, i, j):
        t = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        count = 0
        for o,p in t:
            try:
                count += self.cells[i+o,j+p].get_state()
            except KeyError:
                pass
        return count

    def beat(self, dead_alert):
        cells = self.cells

        for i,j in cells:
            n = self.alive_neights(i,j)
            c = cells[i,j]
            if c.is_alive():
                if n not in (2,3): c.die()
            else:
                if n == 3: c.birth()

        for k in cells:
            cells[k].update_state()

        # Update hero situation in needed
        if self.is_hero_alive() and not self.cells[self.i, self.j].is_alive():
            self.cells[self.i, self.j].color = cell_color
            self.hero_alive = False
        # This fix a bug at dead alert mode but is not the best solution.
        if dead_alert and self.is_hero_alive():
            self.set_hero(self.i, self.j, dead_alert)
        
    def set_hero(self, i, j, dead_alert):
        if self.cells[i,j].is_alive():
            self.i = i
            self.j = j
            color = self._color_at(i, j, dead_alert)
            self.cells[i,j].be_hero(color)
            self.hero_alive = True
            
    def get_hero(self):
        return (self.i, self.j)

    def is_hero_alive(self):
        return self.hero_alive

    def hero_left(self, dead_alert):
        '''If hero can move to the left do it an return True, else return False.
        The dead_alert arg says if the alert is activate or not.'''
        i,j = self.i, self.j
        if self.is_hero_alive() and i > 0 and not self.cells[i-1,j].is_alive():
            self.cells[i,j].be_normal()
            i -= 1
            color = self._color_at(i, j, dead_alert)
            self.cells[i,j].be_hero(color)
            self.i, self.j = i,j
            return True
        return False

    def hero_right(self, dead_alert):
        '''If hero can move to the right do it an return True, else return False.
        The dead_alert arg says if the alert is activate or not.'''
        i,j = self.i, self.j
        if self.is_hero_alive() and i < self.columns - 1 \
                                and not self.cells[i+1,j].is_alive():
            self.cells[i,j].be_normal()
            i += 1
            color = self._color_at(i, j, dead_alert)
            self.cells[i,j].be_hero(color)
            self.i, self.j = i,j
            return True
        return False
            
    def hero_up(self, dead_alert):
        '''If hero can move up do it an return True, else return False.
        The dead_alert arg says if the alert is activate or not.'''
        i,j = self.i, self.j
        if self.is_hero_alive() and j > 0 and not self.cells[i,j-1].is_alive():
            self.cells[i,j].be_normal()
            j -= 1
            color = self._color_at(i, j, dead_alert)
            self.cells[i,j].be_hero(color)
            self.i, self.j = i,j
            return True
        return False
            
    def hero_down(self, dead_alert):
        '''If hero can move down do it an return True, else return False.
        The dead_alert arg says if the alert is activate or not.'''
        i,j = self.i, self.j
        if self.is_hero_alive() and j < self.rows - 1 and not self.cells[i,j+1].is_alive():
            self.cells[i,j].be_normal()
            j += 1
            color = self._color_at(i, j, dead_alert)
            self.cells[i,j].be_hero(color)
            self.i, self.j = i,j
            return True
        return False

    def _color_at(self, i, j, dead_alert):
        '''If dead_alert is off (False) always hero color is returned.'''
        if dead_alert:
            if self.alive_neights(i,j) in (2,3):
                return hero_color
            else:
                return dead_color
        else:
            return hero_color

    def kill_all(self):
        for k in self.cells:
            self.cells[k].die_now()

    def alive_cells(self):
        return len([c for c in self.cells.values() if c.is_alive()])


class Pattern(object):

    def __init__(self, name, kind, period, cells):
        self.name = name
        self.kind = kind
        self.period = period
        self.alive_cells = cells

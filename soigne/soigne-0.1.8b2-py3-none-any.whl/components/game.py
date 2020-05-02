#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame.constants import *

from soigne.container import Component, Event
from soigne.gamegui import GameGui


class DebugInfo:

    position = ()
    items = {}

    def __init__(self, x=5, y=5):
        self.position = (x, y)

    def show(self, window):
        y = 5

        for item in self.items.values():
            text = item[0] + ': ' + item[1]
            font = pygame.font.SysFont('Arial', 15)

            window.blit(font.render(text, 1, item[2]), (5, y + 5))

            y += 15

        pass

    def add(self, caption, info, color):
        self.items[caption] = [caption, info, color]
        pass

    pass


class Game(Component):
    """ Главный класс игры.
    Точка вхождения для взаимодействия пользователя с игрой.
    """
    resources = 'resources/assets/'

    gui: GameGui = None

    # need_show_debug = False
    # debug: DebugInfo = None

    pressed_keys = {}
    need_redraw_gui = True
    stopped = True

    def __init__(self, app):
        super().__init__(app)

        self.app.register('event', 'game_initialization', Event('game_initialization'))
        self.app.register('event', 'game_gui_drawn', Event('game_gui_drawn'))

        self.app.dispatch('quit', on_quit)
        self.app.dispatch('activeevent', on_activeevent)
        self.app.dispatch('keydown', on_keydown)
        self.app.dispatch('keyup', on_keyup)
        self.app.dispatch('mousemotion', on_mousemotion)
        self.app.dispatch('mousebuttonup', on_mousebuttonup)
        self.app.dispatch('mousebuttondown', on_mousebuttondown)
        self.app.dispatch('joyaxismotion', on_joyaxismotion)
        self.app.dispatch('joyballmotion', on_joyballmotion)
        self.app.dispatch('joyhatmotion', on_joyhatmotion)
        self.app.dispatch('joybuttonup', on_joybuttonup)
        self.app.dispatch('joybuttondown', on_joybuttondown)
        self.app.dispatch('videoresize', on_videoresize)
        self.app.dispatch('videoexpose', on_videoexpose)
        self.app.dispatch('userevent', on_userevent)

        self.resources = self.app.path(self.resources)

    def build(self):
        """ """
        self.gui = self.app.get('component', 'gui')
        # self.debug = DebugInfo()

        # Отрисовываем окно игры.
        self.gui.init()

        self.trigger_event('game_initialization', self)

        self.gui.draw(self._handle_drawn_gui)

        return self

    def start(self, handler=None, *args):
        """ Метод запуска цикла обработки игровых событий.
        Обновляет окно игры, запускает обработчики событий.

        :param handler: Обработчик событий
        """
        gui_events = self.gui.component('event')

        self.stopped = False
        while not self.stopped:
            self.gui.component('time').Clock().tick(self.gui.FRAMES)

            self.pressed_keys = self.gui.component('key').get_pressed()

            # if self.pressed_keys[K_LCTRL] and self.pressed_keys[K_d]:
            #     if self.need_show_debug:
            #         self.need_show_debug = False
            #     else:
            #         self.need_show_debug = True

            if handler:
                handler(self, *args)

            for event in gui_events.get():
                if event.type not in self.gui.EVENTS:
                    continue

                self.trigger_event(self.gui.EVENTS[event.type], self, event)

            self.gui.update(self.need_redraw_gui)

            # if self.need_show_debug:
            #     self.debug.show(self.gui.window)
            #     self.gui.update(False)

        # Завершаем игру при нажатии клавиши выхода из игры (или закрытия окна).
        self.gui.close()

    def stop(self):
        self.stopped = True

        # self.gui.close()

    def _handle_drawn_gui(self, *args):
        self.trigger_event('game_gui_drawn', self, *args)


def on_quit(app, event, game, game_event):
    game.stopped = True
    pass


def on_activeevent(app, event, game, game_event):
    pass


def on_keydown(app, event, game: Game, game_event):
    # game.debug.add('Pressed key', game_event.unicode, (0, 0, 0))

    pass


def on_keyup(app, event, game, game_event):
    pass


def on_mousemotion(app, event, game, game_event):
    pass


def _click(app, game, game_event):

    element = game.gui.element(None, *game_event.pos)
    if not element:
        return

    event_name = 'lclick'

    if game_event.button == BUTTON_RIGHT:
        event_name = 'rclick'
    elif game_event.button == BUTTON_MIDDLE:
        event_name = 'mclick'

    method = 'on'

    if game_event.type == 1026:
        method = 'off'

    event = element.__getattribute__(method)
    event(event_name, app, game, game_event)


def on_mousebuttonup(app, event, game, game_event):
    _click(app, game, game_event)


def on_mousebuttondown(app, event, game, game_event):
    _click(app, game, game_event)


def on_joyaxismotion(app, event, game, game_event):
    pass


def on_joyballmotion(app, event, game, game_event):
    pass


def on_joyhatmotion(app, event, game, game_event):
    pass


def on_joybuttonup(app, event, game, game_event):
    pass


def on_joybuttondown(app, event, game, game_event):
    pass


def on_videoresize(app, event, game, game_event):
    pass


def on_videoexpose(app, event, game, game_event):
    pass


def on_userevent(app, event, game, game_event):
    pass


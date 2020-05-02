#!/usr/bin/env python
# coding=utf-8

import abc
import json
import os

import pygame
from pygame.font import Font

from soigne.container import Component, Event, App


class GameGui(Component):
    """ Игровой интерфейс.

    Служит для управления интерфесом игры и обрабатывает игровые события.
    СОдержит в себе набор параметров и методов для добавления элементов интерфеса.
    """

    COMPONENTS = {}
    COLORS = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
    }
    EVENTS = {
        pygame.QUIT: 'quit',
        pygame.ACTIVEEVENT: 'activeevent',
        pygame.KEYDOWN: 'keydown',
        pygame.KEYUP: 'keyup',
        pygame.MOUSEMOTION: 'mousemotion',
        pygame.MOUSEBUTTONUP: 'mousebuttonup',
        pygame.MOUSEBUTTONDOWN: 'mousebuttondown',
        pygame.JOYAXISMOTION: 'joyaxismotion',
        pygame.JOYBALLMOTION: 'joyballmotion',
        pygame.JOYHATMOTION: 'joyhatmotion',
        pygame.JOYBUTTONUP: 'joybuttonup',
        pygame.JOYBUTTONDOWN: 'joybuttondown',
        pygame.VIDEORESIZE: 'videoresize',
        pygame.VIDEOEXPOSE: 'videoexpose',
        pygame.USEREVENT: 'userevent',
    }

    FRAMES = 30

    DOUBLEBUF = pygame.DOUBLEBUF
    FULLSCREEN = -pygame.FULLSCREEN
    HWSURFACE = pygame.HWSURFACE
    NOFRAME = pygame.NOFRAME
    OPENGL = pygame.OPENGL
    RESIZABLE = pygame.RESIZABLE
    SCALED = pygame.SCALED

    dimensions = (800, 450)
    caption = 'GuiComponent'
    icon = None
    background = 'black'
    centred = True
    font = 'Arial'
    flags = 0
    depth = 0
    display = 0

    window = None
    element_states = None
    elements = {}

    def __init__(self, app):
        Component.__init__(self, app)
        pygame.init()
        self._register_components()

        # Регистрация событий игрвого интерфейса.
        self.app.register('event', 'quit', Event('quit'))
        self.app.register('event', 'activeevent', Event('activeevent'))
        self.app.register('event', 'keydown', Event('keydown'))
        self.app.register('event', 'keyup', Event('keyup'))
        self.app.register('event', 'mousemotion', Event('mousemotion'))
        self.app.register('event', 'mousebuttonup', Event('mousebuttonup'))
        self.app.register('event', 'mousebuttondown', Event('mousebuttondown'))
        self.app.register('event', 'joyaxismotion', Event('joyaxismotion'))
        self.app.register('event', 'joyballmotion', Event('joyballmotion'))
        self.app.register('event', 'joyhatmotion', Event('joyhatmotion'))
        self.app.register('event', 'joybuttonup', Event('joybuttonup'))
        self.app.register('event', 'joybuttondown', Event('joybuttondown'))
        self.app.register('event', 'videoresize', Event('videoresize'))
        self.app.register('event', 'videoexpose', Event('videoexpose'))
        self.app.register('event', 'userevent', Event('userevent'))

    def init(self):
        """ Метод инициализации игрового интерфейса.

        Регистрирует состояния элементов.
        Устанавливает параметры отрисовки игровго интерфейса и окна.
        """

        if self.centred:
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.window = self.component('display').set_mode(
            self.dimensions,
            flags=self.flags,
            depth=self.depth,
            display=self.display
        )

        return self

    def color(self, name):
        """ Мотод получения цвета из цветовой палитры. """

        if name not in self.COLORS:
            raise NameError('Unknown colour <' + str(name) + '> name. You can use only: '
                            + str.join(', ', self.COLORS.keys()) + '.')

        return self.COLORS[name]

    def component(self, name='self'):
        """ Мотод получения компонента игрвого интерфеса. """

        if name == 'self':
            return self

        if name not in self.COMPONENTS:
            raise NameError('Unknown gui <' + name + '> component. There are only '
                            + str.join(', ', self.COMPONENTS.keys()) + ' component in GUI class.')

        return self.COMPONENTS[name]

    def element(self, name=None, x=None, y=None):
        """ Возвращает элементы интерфеса.

        При переданом имени, эллемент будет возвращён из списка по имени.

        В случае указания координат позиции, в списке будет найден эллемент,
        который пересекает указанную позицию.
        """

        element = None

        if name and x is None and y is None:
            if name not in self.elements:
                raise NameError('Unknown <' + name + '> element.')

            element = self.elements[name]
        elif x >= 0 and y >= 0:
            for el in self.elements.values():
                if self.check_position(el.position, el.get_rect(), x, y):
                    element = el

        return element

    @staticmethod
    def check_position(position, dimensions, x, y):
        return position[0] < x < position[0] + dimensions.width and position[1] < y < position[1] + dimensions.height

    def set_colors(self, **colors):
        """ Добавляет переданные цвета к цветовой палитре. """

        for name, color in colors.items():
            if type(color) is not tuple:
                raise TypeError('Invalid color parameters. Expected tuple, ' + str(type(color)) + ' given.')

            self.COLORS[name] = color

        pass

    def set_dimensions(self, width=800, height=450):
        """ Устаналвивает размеры окна приложения.

        Небходимо вызывать перед инициализацией интерфеса.
        """

        self.dimensions = (width, height)

        pass

    def set_centered(self, centered=True):
        """ Устаналвивает правило, что окно приложенияи необходимо отрисовывть в центре экрана.

        Небходимо вызывать перед инициализацией интерфеса.
        """

        self.centred = centered

        pass

    def set_flags(self, flags: int):
        """ Устаналвивает флаги отрисовки интерфейса.
        """

        self.flags = flags

        pass

    def set_depth(self, depth: int):
        """ Устаналвивает количество бит для цвета.

        Обычно лучше не передавать аргумент глубины. По умолчанию будет установлена
        наилучшая и самая быстрая глубина цвета для системы.
        """

        self.depth = depth

        pass

    def set_display(self, display: int):
        """ Устаналвивает флаги отрисовки интерфейса.
        """

        self.display = display

        pass

    def set_icon(self, path, size=(32, 32)):
        """ Устаналвивает иконку окна приложения. """

        if not path:
            return False

        self.icon = self.component('image').load(path).convert_alpha()  # Создаём (загружаем) иконку

        self.icon.set_colorkey(self.color('black'))
        self.icon.blit(self.icon, size)

        return self.component('display').set_icon(self.icon)

    def set_caption(self, caption):
        """ Устаналвивает заголовок окна приложения. """

        self.caption = caption if caption else self.app.NAME

        return self.component('display').set_caption(self.caption)

    def set_background(self, color):
        """ Устаналвивает фон окна приложения. """

        if not color:
            return False

        self.background = color

        return self.window.fill(self.color(self.background))

    def add(self, name, element, x=0, y=0, parent=None, area=None, flags=0):
        """ Добавляет элемент интерфеса.

        В качестве элемента принимает объект типа pygame.Surface.

        Если был передан объект типа app.gamegui.Element в список добавляется данный объект,
        а указанные параметры после него перезаписывают соответствующие параметры указанного объекта.
        """

        if isinstance(element, pygame.Surface):
            self.elements[name] = Element(element, name, x, y, area, flags, parent)
        elif isinstance(element, Element):
            element.set_name(name)
            element.set_position(x, y)
            element.set_parent(parent)
            element.set_area(area)
            element.set_flags(flags)

            self.elements[name] = element
        else:
            raise TypeError('Unknown type of element ' + str(type(element))
                            + ". Тип элемента может быть <class 'pygame.Surface'> или <class 'app.gamegui.Element'>")

        with open(self.app.path('resources/element_states.json'), "r") as element_states:
            states = json.load(element_states)

        for event in Element.EVENTS:
            event_name = element.name + '_' + event

            self.app.register('event', 'on_' + event_name, Event('on_' + event_name))
            self.app.register('event', 'off_' + event_name, Event('off_' + event_name))

        for state in states:
            if element.name in state['name']:
                element.set_state(state['name'].replace(element.name, '').strip('.'), state['state'])

        pass

    def reset_elements(self):
        """ Очищает список элементов игрового интерфейса. """

        # for element in self.elements:
        #     for event in Element.EVENTS:
        #         self.app.remove_event('on_' + element + '_' + event, no_errors=True)
        #         self.app.remove_event('off_' + element + '_' + event, no_errors=True)
        #
        #     del self.elements[element]
        self.elements = {}

        pass

    def draw_elements(self):
        """ Отрисовывает текущие зарегистрированые элементы интерфейса.
        """

        for element in self.elements.values():
            surface = self.window

            if element.parent is not None:
                surface = element.parent.subsurface(element.get_rect())

            x, y = self.component('mouse').get_pos()
            if element.need_change_hover_state and self.check_position(element.position, element.get_rect(), x, y):
                element.change_state(self.app, 'on', 'hovered')

            surface.blit(*element.surface())

        pass

    def draw(self, callback=None, *args):
        """ Отрисовывает интерфейс приложения.

        Вызывает переданный обработчик после отрисовки.
        """

        self.update()

        if callable(callback):
            callback(*args)

        pass

    def update(self, redraw_gui=True):
        """ Обновляет игрвой интерфейс.

        При указанном ложном значении параметра redraw_gui элементы интерфейса перересованны не будут.
        """

        if redraw_gui:
            if self.icon:
                self.component('display').set_icon(self.icon)
            self.component('display').set_caption(self.caption)

            self.window.fill(self.color(self.background))

            self.draw_elements()

        self.component('display').update()

        pass

    def close(self):
        """ Завершение обработки игрвых событий и очистка игрвого интерфейса. """

        self.reset_elements()

        return self.component('display').quit()

    def _register_components(self):
        """ Регистрирует используемые компоненты для быстрого доступа. """

        self.COMPONENTS = {
            "display": pygame.display,
            "image": pygame.image,
            "drawer": pygame.draw,
            "event": pygame.event,
            "time": pygame.time,
            "key": pygame.key,
            "mouse": pygame.mouse,
        }


class Layout:
    gui: GameGui = None
    app: App = None

    def __init__(self, gui):
        self.gui = gui
        self.app = gui.app

    def draw(self):
        self.gui.reset_elements()

        for element in self.elements():
            self.gui.add(*element)

        self.events()

    @abc.abstractmethod
    def elements(self):
        return []

    @abc.abstractmethod
    def events(self):
        pass


# class Sprites(pygame.sprite.Group):
#     def __init__(self, *sprites):
#         super().__init__(*sprites)
#
#     pass
#
#
# class Sprite(pygame.sprite.Sprite):
#     def __init__(self):
#         pass


class Element:
    """ Элемент интерфейса.
    """
    LEFT_CLICK_EVENT = 'lclick'
    MIDDLE_CLICK_EVENT = 'mclick'
    RIGHT_CLICK_EVENT = 'rclick'
    MOUSEMOTION_EVENT = 'mousemotion'

    EVENTS = [
        LEFT_CLICK_EVENT,
        MIDDLE_CLICK_EVENT,
        RIGHT_CLICK_EVENT,
        MOUSEMOTION_EVENT,
    ]

    _surface = None

    name = ''
    position = (0, 0)
    area = None
    flags = 0
    parent = 0

    states = {}

    inited = False
    need_change_hover_state = True

    def __init__(self, surface, name='', x=0, y=0, area=None, flags=0, parent=None):
        self._surface = surface
        self.name = name
        self.position = (x, y)
        self.area = area
        self.flags = flags
        self.parent = parent

        self.states = {}

        self.inited = True

    def surface(self):
        return [self._surface, self.position, self.area, self.flags]

    def get_rect(self):
        return self._surface.get_rect()

    def get_dimensions(self):
        return self.get_rect().width, self.get_rect().height

    def set_name(self, name):
        self.name = name
        pass

    def set_position(self, x, y):
        self.position = (x, y)
        pass

    def set_area(self, area):
        self.area = area
        pass

    def set_flags(self, flags):
        self.flags = flags
        pass

    def set_parent(self, parent):
        self.parent = parent
        pass

    def set_state(self, name, state):
        self.states[name] = state

        pass

    @abc.abstractmethod
    def change_state(self, app: App, event_type, event_name, *options):
        pass

    def on(self, event_name, app, *options):
        self._trigger('on', event_name, app, *options)

    def off(self, event_name, app, *options):
        self._trigger('off', event_name, app, *options)

    def _trigger(self, name, event_name, app: App, *options):
        """ Изменяет состояние элемента, а также вызывает обработчики соотвествующего события.
        """

        self.change_state(app, name, event_name, *options)

        event_name = name + '_' + self.name + '_' + event_name
        if app.is_triggerable(event_name):
            app.trigger_event(event_name, *options)

    def _get_state(self, name):
        if name in self.states:
            return self.states[name]

        return {}


class Field(Element):

    def __init__(self, width, height, background=(0, 0, 0), name='', x=0, y=0, *args, **kwargs):
        super().__init__(pygame.Surface((width, height)), name, x, y, *args, **kwargs)

        self.set_background(background)

    def set_background(self, background):
        if type(background) is tuple:
            self._surface.fill(background)

            return

        background = pygame.transform.scale(pygame.image.load(background), self.get_dimensions())

        self._surface.blit(background, (0, 0))
        self._surface.set_colorkey((0, 0, 0))

        pass

    def change_state(self, app: App, event_type, event_name, *options, **state):
        pass


# class Circle(Element):
#     radius = 0
#     background = 0
#
#     def __init__(self, radius, background=(0, 0, 0), name='', x=0, y=0, *args, **kwargs):
#         super().__init__(pygame.Surface((radius * 2, radius * 2)), name, x, y, *args, **kwargs)
#
#         self.radius = radius
#         self.background = background
#
#         self.draw()
#
#     def set_radius(self, radius):
#         self.radius = radius
#
#     def set_background(self, background):
#         self.background = background
#
#     def redraw(self):
#         pygame.draw.circle(self._surface, self.background, (self.radius, self.radius), self.radius)
#         self._surface.set_colorkey((0, 0, 0))
#
#     draw = redraw
#
#     def change_state(self, app: App, event_type, event_name, *options, **state):
#         pass


class Text(Element):
    """ Текстовый элемент игрового интерфейса <app.gamegui.Text(Element)>.
    """

    text = ''
    color = (0, 0, 0)
    fontsize = 15
    font: Font = None
    fontname = 'Arial'
    italic = False
    bold = False
    underline = False

    def __init__(self, text, color=(0, 0, 0), fontsize=15, font='Arial', italic=False, bold=False, underline=False):
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.fontname = font
        self.italic = italic
        self.bold = bold
        self.underline = underline

        self.font = pygame.font.SysFont(self.fontname, self.fontsize)

        self.font.set_italic(self.italic)
        self.font.set_bold(self.bold)
        self.font.set_underline(self.underline)

        super().__init__(self.font.render(self.text, 1, self.color))

    def change_state(self, app: App, event_type, event_name, *options, **state):
        pass


class Button(Field):
    """ Кнопка игрового интерфейса <app.gamegui.Button(Element)>

    Для инициализации кнопки первым параметром необходимо передать обработчик нажатия кнопки.
    Помимо него указать следующие параметры
        *text* - отображаемый текст на кнопке
        *width* - ширина кнопки
        *height* - высота кнопки
        *color* - цвет текста
        *background* - цвет кнопки
        *font* - шрифт текста
        *fontsize* - размер текста
    """

    text: Text = None

    def __init__(self, text, *args, **kwargs):

        color, fontsize, font = (255, 255, 255), 15, 'Arial'

        if 'color' in kwargs:
            color = kwargs['color']
            kwargs.pop('color')

        if 'fontsize' in kwargs:
            fontsize = kwargs['fontsize']
            kwargs.pop('fontsize')

        if 'font' in kwargs:
            font = kwargs['font']
            kwargs.pop('font')

        super().__init__(*args, **kwargs)
        self.set_text(text, color, fontsize, font)

    def change_state(self, app: App, event_type, event_name, *options):
        if event_type != 'on':
            return

        state = self._get_state(event_name)

        if len(state) == 0:
            return

        text = self.text.text
        color = self.text.color
        fontsize = self.text.fontsize
        font = self.text.fontname
        italic = self.text.italic
        bold = self.text.bold
        underline = self.text.underline

        if 'background' in state:
            background = state['background']

            if len(background) != 3:
                background = app.path(background)

            self.set_background(background)

        if 'text' in state:
            text = state['text']

        if 'color' in state:
            color = state['color']

        if 'fontsize' in state:
            fontsize = state['fontsize']

        if 'font' in state:
            font = state['font']

        if 'italic' in state:
            italic = state['italic']

        if 'bold' in state:
            bold = state['bold']

        if 'underline' in state:
            underline = state['underline']

        if 'position' in state:
            self.set_position(*state['position'])

        self.set_text(text, color, fontsize, font, italic, bold, underline)
        self.need_change_hover_state = False

    def set_text(self, text, color=(255, 255, 255), fontsize=15, font='Arial', italic=False, bold=False,
                 underline=False):
        if type(text) is not Text:
            self.text = Text(text, color, fontsize, font, italic, bold, underline)
        else:
            self.text = text

        text_width, text_height = self.text.get_dimensions()
        width, height = self.get_dimensions()

        self.text.set_position(width / 2 - text_width / 2, height / 2 - text_height / 2)

        self._surface.blit(*self.text.surface())


class Image(Element):
    filename = ''

    def __init__(self, filename, colorkey=(0, 0, 0), width=0, height=None, *args, **kwargs):
        self.filename = filename

        image = pygame.image.load(filename)

        if width > 0 and (type(height) is not int or height <= 0):
            w = image.get_rect().width
            h = image.get_rect().height
            k = width / w
            height = int(h * k)

        if height > 0 and (type(width) is not int or width <= 0):
            h = image.get_rect().height
            w = image.get_rect().width
            k = height / h
            width = int(w * k)

        image = pygame.transform.scale(image, (width, height))

        super().__init__(image, *args, **kwargs)

        self.set_colorkey(colorkey)

    def convert(self):
        return self._surface.convert()

    def convert_alpha(self):
        return self._surface.convert_alpha()

    def get_colorkey(self):
        return self._surface.get_colorkey()

    def get_alpha(self):
        return self._surface.get_alpha()

    def set_colorkey(self, color):
        self._surface.set_colorkey(color)

        return self

    def set_alpha(self, value, flags=0):
        self._surface.set_alpha(value, flags)

        return self

    def change_state(self, app: App, event_type, event_name, *options):
        pass

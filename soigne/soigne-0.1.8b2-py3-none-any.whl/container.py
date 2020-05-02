#!/usr/bin/env python
# coding=utf-8


class App:
    """ Класс обработки приложения.
    """

    # Константы приложения.
    NAME = 'python-application'
    DESCRIPTION = 'Python application'
    URL = ''
    VERSION = 'v0.1.0'

    _path = './'

    _components = {}
    _events = {}

    def __init__(self, path='./'):
        # Регистрация события начала и окончания сборки приложения.
        self.register('event', 'application_build', Event('application_build'))
        self.register('event', 'application_built', Event('application_built'))

        self._path = path

        pass

    def path(self, path):
        return self._path + '/' + path

    def get(self, attr, name=None):
        attribute = '_' + attr + 's'

        if attribute not in dir(self):
            raise NameError('Unknown application attribute <' + attr + '>.')

        attribute = self.__getattribute__(attribute)

        if name is None:
            return attribute

        if name not in attribute:
            raise NameError('Unknown application ' + attr + ' <' + name + '>.')

        return attribute[name]

    def dispatch(self, event, handler):
        """ Сообщает обработчик событию.
        Обращается к регистру событий приложения. при наличии такового события
        добавляет переданный обработчик.

        В случае отсутствия события возникает ошибка.
        """
        if event not in self._events:
            raise SystemError('Unknown <' + event + '> event.')

        self._events[event].append_handler(handler)

    def register_events(self, options):
        """ Регистрирует события приложения.

        В качестве параметров options необходимо передавать первым элементом имя события,
        а вторым - его объект.

        Если был передан не верный тип объекта события возникает ошибка.
        """
        if type(options[1]) is not Event:
            raise TypeError('Registered event mast be type of app.container.Event')

        self._events[options[0]] = options[1]

    def register_components(self, options):
        """ Регистрирует компоненты приложения.

        В качестве параметров options необходимо передавать имя компонента.

        Если был передан не верный тип объекта компонента возникает ошибка.
        """
        if not issubclass(options[1], Component):
            raise TypeError('Registered component mast be type of app.container.Component')

        component = options[1]

        self._components[options[0]] = component(self)

    def build(self, component):
        """ Метод сборки приложения.

        :param component: Основной компонент, исполняющий основные функции приложения.
        :param args: Аргументы необходимые для выполнения приложения.
        """
        self.trigger_event('application_build')  # Вызываем обработку начала сборки приложения.

        component = self.get('component', component)
        component = component.build()

        # thread = threading.Thread(
        #     name=App.NAME,
        #     target=component.build,
        #     args=args,
        #     daemon=True
        # )
        #
        # thread.start()
        # thread.join()

        self.trigger_event('application_built')  # Вызываем обработку окончания сборки приложения.

        return component

    def register(self, t, *options, registerer=None):
        """ Регистрирует атрибуты приложения.

        Именем атрибута может быть лишь строка, состоящая из букв латинского алфовита,
        цыфр и символа нижнего подчёркивания.

        В случае если не указан регистратор и если имя атрибута приложения указано не верно, возникает ошибка.
        """
        attribute = 'register_' + t + 's'

        # Проверяем правильность указания атрибута
        if attribute not in dir(App) and registerer is None:
            raise NameError('Unknown registration name <' + t + '>.')

        # Вызываем указанный регистратор с указанными параметрами и
        # передаём объект приложения для дальнейшей регистрации.
        if callable(registerer):
            self.__setattr__('_' + t + 's', registerer(self, options[0], *options))

            return

        # Иначе регистрируем шаттными методами.
        registerer = self.__getattribute__(attribute)
        registerer(options)

    def is_triggerable(self, name):
        return name in self._events

    def trigger_event(self, name, *args, **kwargs):
        """ Вызывает обработчики события.
        """
        if name not in self._events:
            raise SystemError('Unknown <' + name + '> event.')

        self._events[name].trigger(self, *args, **kwargs)

    def remove_event(self, name, no_errors=False):
        """ Удаляет событие.
        """
        if name not in self._events and not no_errors:
            raise SystemError('Unknown <' + name + '> event.')

        del self._events[name]

    pass


class Component:
    app = App

    def __init__(self, app):
        self.app = app

    def trigger_event(self, name, *args, **kwargs):
        self.app.trigger_event(name, *args, **kwargs)

    pass


class Event:
    name = ''
    handlers = []

    data = None

    def __init__(self, name):
        self.name = name
        self.handlers = []

    def append_handler(self, handler):
        self.handlers.append(handler)

        pass

    def trigger(self, app, *args, **kwargs):
        for handler in self.handlers:
            handler(app, self, *args, **kwargs)

        pass

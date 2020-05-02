"""Base application class for all your needs.

Only one application can exist in one interpreter instance.
You can use instance of this class without being inherited, but expect reduced
functionality.
"""

from __future__ import annotations

import time
import typing
import weakref

from typing import (
    Dict,
    Type,
    Optional,
)

# TODO: move out into ioloop integration framework
from tornado import ioloop

import eaf.core
import eaf.errors

from eaf.render import Renderer


if typing.TYPE_CHECKING:
    from eaf.state import State  # pragma: no cover


class Task:
    def __init__(self, func, args=None, kwargs=None, oneshot=True):
        self._func = func
        self._args = args or ()
        self._kwargs = kwargs or {}

        self._done = False
        self._successul = False

    @property
    def done(self):
        return self._done

    @property
    def successful(self):
        return self._successful

    def __call__(self):
        self._done = True

        error = None
        result = None

        try:
            result = self._func(*args, **kwargs)
        except Exception as e:
            error = e

        if error:
            raise error
        self._successul = True

        return result


class Loop:
    def add_callback(self, callback, args, kwargs):

        raise NotImplementedError

    def start(self):
        pass

    def stop(self):
        pass


class SimpleLoop(Loop):
    def __init__(self):
        self._running = False
        self._tasks = []

    def add_callback(self, callback, args=None, kwargs=None):

        self._tasks.append(Task(callback, args, kwargs))

    def start(self):
        self._running = True

        while self._running:
            for task in self._tasks[:]:
                if task.oneshot and task.done:
                    self._tasks.remove(task)
                else:
                    try:
                        task()
                    except Exception as e:
                        LOG.exception("Task failed")

    def stop(self):
        self._running = False


class Application:
    """Base application class.

    Provides state manipulation routines. Subclasses are required to provide
    renderer and event queue because there is no enterprise solutions without
    input and output.
    """

    __instance__ = None
    """Instance of the current application."""

    def __init__(
        self, renderer: Renderer = Renderer("dummy"), event_queue=None, fps: int = 30
    ):
        self._renderer = renderer
        self._event_queue = event_queue

        self._state: Optional[State] = None
        self._states: Dict[str, State] = {}
        self._fps = fps
        self._time = time.perf_counter()
        self._dt = 0.00001

        self._ioloop = ioloop.IOLoop.current()
        tick = weakref.WeakMethod(self.tick)
        self._pc = ioloop.PeriodicCallback(lambda: tick()(), 1000 / self._fps)
        self._pc.start()

        if Application.__instance__ is None or Application.__instance__() is None:
            Application.__instance__ = weakref.ref(self)

    def tick(self):
        """Executes every frame."""

        if not self._state:
            return

        self._state.events()
        self._state.update()
        self._state.render()

    @classmethod
    def current(cls) -> Application:
        """Return the current application instance."""

        if cls.__instance__ is None or cls.__instance__() is None:
            raise eaf.errors.ApplicationNotInitializedError()

        return cls.__instance__()

    @property
    def state(self) -> State:
        """Current state getter."""

        if self._state:
            return self._state
        else:
            raise eaf.errors.ApplicationIsEmpty()

    @state.setter
    def state(self, name: str):
        """Current state setter."""

        if name in self._states:
            self._state = self._states[name]
        else:
            raise eaf.errors.ApplicationStateIsNotRegistered(name)

    @property
    def states(self) -> Dict[str, State]:
        """State names to State classes mapping."""

        return self._states

    def register(self, state: Type[State]):
        """Add new state and initiate it with owner application.

        :param state: state class to register
        """

        name = state.__name__
        state_object = state(self)
        self._states[name] = state_object

        # NOTE: State cannot instantiate in State.__init__ objects that
        #       want access to state because there is no instance at creation
        #       moment. For such objects state can declare it's 'postinit'
        #       method.
        # NOTE: Objects in state on postinit phase can try access current
        #       state, so it must be used as current at postinit state, and
        #       rolled back after.
        previous_state = self._state
        self._state = self._states[name]

        state_object.postinit()

        if len(self._states) > 1:
            self._state = previous_state

    def deregister(self, name: str):
        """Remove existing state."""

        state = self._states.pop(name)
        del state

    def trigger_state(self, state: str, *args, **kwargs):
        """Change current state and pass args and kwargs to it."""

        self.state = state  # type: ignore
        self.state.trigger(*args, **kwargs)

    def trigger_reinit(self, name: str):
        """Deregister state, register again and make it current."""

        state = self.states[name].__class__

        self.deregister(name)
        self.register(state)
        self.state = name  # type: ignore

    @property
    def renderer(self) -> Renderer:
        """Application's renderer getter."""

        return self._renderer

    @property
    def event_queue(self):
        """Application's event queue getter."""

        return self._event_queue

    @property
    def fps(self) -> int:
        """Desired FPS getter."""

        return self._fps

    @fps.setter
    def fps(self, val: int):
        """Desired FPS setter."""

        self._fps = int(val)

    def start(self):
        """Start main application loop."""

        if not self._state:
            raise eaf.errors.ApplicationIsEmpty()

        self._ioloop.start()

    def stop(self):
        """Stop application."""

        self._pc.stop()
        self._ioloop.add_callback(self._ioloop.stop)


def current() -> Application:
    """Current application getter."""

    return Application.current()

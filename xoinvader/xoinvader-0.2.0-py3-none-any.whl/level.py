"""Module for creating and maintaining xoinvader levels.

One level consists of several files that can be packed into directory or ZIP file.

Without structure:
- levels
  - first-level.lv
  - first-level.bg
  - first-level.ev
  ...

Directory or zip archive
- levels
  - first-level.zip
  - second-level
    - second-level.lv
    - second-level.bg
    - second-level.ev

Usage:
level = Level.from_file("levels/first-level.zip")
level = Level.from_file("levels/second-level/second-level.lv")

state.add(level)
level.start()
"""


class LevelSyntaxError(Exception):
    def __init__(self, line, message):

        self.line = line
        self.message = message

        super().__init__(f"[line: {line}] {message}")


class LevelFormat:
    """Level file format.

    # Comments and whitespaces between sections are ignored
    # Comments cannot be placed within blocks
    # first meaningful line must be in format {engine}:{filespec}.
    xo1:level
    # or
    xo1:level@1

    If background chunks defined in separate file, you should specify it:
    bg:path/to/level-1.bg
    # TODO: inplace definition

    If events defined in separate file, you should specify it:
    ev:path/to/level-1.ev
    """

    ENGINE_XO1 = "xo1"
    SUPPORTED_ENGINES = [
        ENGINE_XO1,
    ]

    FORMAT_LEVEL = "level"
    """Generic level format."""

    FORMAT_LEVELv1 = "level@1"

    SUPPORTED_FORMATS = [
        FORMAT_LEVEL,
        FORMAT_LEVELv1,
    ]

    SEP = ":"
    COMMENT = "#"
    EVENT = f"ev{SEP}"
    BACKGROUND = f"bg{SEP}"

    def __init__(self):
        self._parsed = False
        self._current_block = None
        self._line = 0

        self._engine = None
        self._format = None

        self._bg_name = None
        self._bg_file = None

    def raise_syntax_error(self, message):
        raise LevelSyntaxError(self.line, message)

    def parse(self, filename):
        with open(filename) as level:
            self._file = level

            self.parse_magic()
            self._parsed = True

            print(self.as_string())
            # self.parse_background()
            # self.parse_events()
            # self.parse_level()

        # first meaningful line must contain format

    def _advance(self):
        if self._parsed:
            raise Exception("File already parsed")

        self.line += 1

        return self._file.readline().strip()

    def _split(self, line):
        return map(str.strip, line.split(self.SEP))

    def _splittable(self, line):
        return line and self.SEP in line

    def parse_magic(self):
        line = self._advance()
        if self._splittable(line):
            engine, filespec = self._split(line)
            if engine not in self.SUPPORTED_ENGINES:
                self.raise_syntax_error(f"engine '{engine}' is not supported")

            if filespec not in self.SUPPORTED_FORMATS:
                self.raise_syntax_error(f"format {filespec} is not supported")

            self._engine = engine
            self._format = filespec

    def parse_event(self, header):
        if not self._splittable(header):
            self.raise_syntax_error("can't parse event header")

        _, ev_name = self._split(header)
        if ev_name:
            self._ev_name = ev_name
            self._ev_file = open(self._ev_name)
        # else defined in level file

    def parse_background(self, header):
        if not self._splittable(header):
            self.raise_syntax_error("can't parse background header")

        _, bg_name = self._split(header)
        if bg_name:
            self._bg_name = bg_name
            self._bg_file = open(self._bg_name)
        # else defined in level file

    def as_string(self):
        if not self._parsed:
            raise Exception("File is not fully parsed")

        return f"""
        {self._engine}{self.SEP}{self._format}\n

        {self.EVENT}
        """


class Level(object):
    """Container for level event sequence and resources.

    Intended to use as just container, but may be subclassed. It's useful in
    order to add methods for creating concrete animations and events, such as
    spawning actual enemies, bonuses, initiating boss fights and so on.

    :param int speed: relative speed of the wave. Means how fast time advances.
    The faster time advances, the shorter the delays between events triggering.
    :param dict events: map from relative time in event to event starting
    function.
    :param bool running: if event sequence currently advances.
    """

    def __init__(self, speed=0):
        self._running = False
        self._counter = 0
        self._speed = speed
        self._events = {}
        self._event_timeouts = []

    @property
    def speed(self):
        """Relative wave's speed.

        :getter: yes
        :setter: yes
        :type: int
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """Setter."""
        self._speed = value

    @property
    def running(self):
        """If event sequence currently advances.

        :getter: yes
        :setter: no
        :type: bool
        """
        return self._running

    def add_event(self, time, callback):
        """Add event to some point in time.

        :param int time: point in time relative to level start when to run
        `callback`. Callback is fired when `_counter` exceeds provided value
        :param function callback: callback to be fired when wave reaches `time`
        """
        self._events.setdefault(time, []).append(callback)

    def start(self):
        """Start the level.

        Resets the counter, recomputes the list of event timeouts and sets the
        `running` property to `True`.
        """

        self._running = True
        self._counter = 0
        self._event_timeouts = sorted(self._events)

    def update(self):
        """Update the counter and fire appropriate events.

        Function is doing anything useful only when the Level has been started
        earlier, i.e. currently in running state.
        Function updates current timer and fires all events, which timeouts have
        expired. If there's no more events in the queue, the running state
        terminates and object goes to sleep.
        Time counter is increased by `_speed` value at each call of the
        fucntion.
        """

        if not self._running:
            return

        self._counter += self._speed
        while self._event_timeouts[0] <= self._counter:
            current_timeout = self._event_timeouts[0]
            for callback in self._events[current_timeout]:
                callback()
            del self._event_timeouts[0]
            if not self._event_timeouts:
                self._running = False
                break

import curses
import itertools
import signal
import threading

from rockart import Canvas
from rockart_examples import RockartExamplesValueError
from rockart_examples.life.game import Game


def render_game(game, terminal_rows, terminal_columns):
    field_border = 1
    field_padding = 1
    cell_size = 4
    cell_border = 1

    min_canvas_size = 2 * (field_border + field_padding)
    min_terminal_rows = \
        min_canvas_size // Canvas.CELL_HEIGHT \
        + min(min_canvas_size % Canvas.CELL_HEIGHT, 1)
    min_terminal_columns = \
        min_canvas_size // Canvas.CELL_WIDTH \
        + min(min_canvas_size % Canvas.CELL_WIDTH, 1)
    if terminal_rows < min_terminal_rows:
        raise RockartExamplesValueError(
            f"`terminal_rows` must be greater or equal {min_terminal_rows}"
        )
    if terminal_columns < min_terminal_columns:
        raise RockartExamplesValueError(
            f"`terminal_columns` must be greater or equal {min_terminal_columns}"
        )

    canvas = Canvas.of_size(terminal_rows, terminal_columns - 1)

    frame_min_x = \
        max(
            canvas.width // 2 - game.columns // 2 * cell_size - (field_border + field_padding),
            0
        )
    frame_max_x = \
        min(
            canvas.width // 2 + (game.columns - game.columns // 2) * cell_size + field_padding,
            canvas.width - 1
        )
    frame_min_y = \
        max(
            canvas.height // 2 - game.rows // 2 * cell_size - (field_border + field_padding),
            0
        )
    frame_max_y = \
        min(
            canvas.height // 2 + (game.rows - game.rows // 2) * cell_size + field_padding,
            canvas.height - 1
        )
    for x in range(frame_min_x, frame_max_x + 1):
        canvas.paint(x, frame_min_y)
        canvas.paint(x, frame_max_y)
    for y in range(frame_min_y, frame_max_y + 1):
        canvas.paint(frame_min_x, y)
        canvas.paint(frame_max_x, y)

    for game_row, game_column in itertools.product(range(game.rows), range(game.columns)):
        is_alive = game.is_cell_alive(game_row, game_column)
        if not is_alive:
            continue

        cell_x = (game_column - game.columns // 2) * cell_size + (canvas.width // 2)
        cell_y = (game_row - game.rows // 2) * cell_size + (canvas.height // 2)

        for local_x in range(cell_border, cell_size - cell_border):
            for local_y in range(cell_border, cell_size - cell_border):
                x = cell_x + local_x
                if x < field_border + field_padding:
                    continue
                if x >= canvas.width - (field_border + field_padding):
                    continue

                y = cell_y + local_y
                if y < field_border + field_padding:
                    continue
                if y >= canvas.height - (field_border + field_padding):
                    continue

                canvas.paint(x, y)

    return canvas.render()


def run_gui(is_shutdown_required=None):
    if is_shutdown_required is None:
        is_shutdown_required = threading.Event()
        def handle_shutdown_signal(*args):
            is_shutdown_required.set()
        signal.signal(signal.SIGINT, handle_shutdown_signal)
        signal.signal(signal.SIGTERM, handle_shutdown_signal)

    game = Game(30, 30)
    game.initialize()

    def interact(screen):
        curses.curs_set(False)
        curses.use_default_colors()

        while not is_shutdown_required.is_set():
            rows, columns = screen.getmaxyx()
            try:
                frame = render_game(game, rows, columns)
            except RockartExamplesValueError:
                frame = ""

            screen.erase()
            try:
                screen.addstr(0, 0, frame)
            except curses.error:
                continue
            screen.refresh()

            curses.napms(50)
            game.move()
    curses.wrapper(interact)

import itertools
import random

from rockart_examples import (
    RockartExamplesException,
    RockartExamplesIndexError,
    RockartExamplesValueError
)


class Game:
    __INITIAL_LIFE_PROBABILITY = 0.1
    __NEIGHBOUR_LIFE_PROBABILITY = 0.3


    def __init__(self, rows, columns, *args, seed=None, **kwargs):
        super().__init__(*args, **kwargs)

        if rows < 0:
            raise RockartExamplesValueError("`rows` must be positive")

        if columns < 0:
            raise RockartExamplesValueError("`columns` must be positive")

        self.__is_initialized = False
        self.__epoch = None
        self.__rows = rows
        self.__columns = columns
        self.__field = [
            [False]*self.__columns for _ in range(self.__rows)
        ]
        self.__hidden_field = [
            [False]*self.__columns for _ in range(self.__rows)
        ]
        self.__random = random.Random(seed)

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns


    @property
    def is_initialized(self):
        return self.__is_initialized

    @property
    def epoch(self):
        if not self.__is_initialized:
            raise RockartExamplesException("Initialize game first")

        return self.__epoch

    def is_cell_alive(self, row, column):
        if not self.__is_initialized:
            raise RockartExamplesException("Initialize game first")

        if not 0 <= row < self.__rows:
            raise RockartExamplesIndexError(
                f"`row` must belong to a range [0; {self.__rows - 1}])"
            )

        if not 0 <= column < self.__columns:
            raise RockartExamplesIndexError(
                f"`column` must belong to a range [0; {self.__columns - 1}])"
            )

        return self.__field[row][column]

    def initialize(self):
        if self.__is_initialized:
            raise RockartExamplesException("Game is initialized already")

        for row, column in itertools.product(range(self.__rows), range(self.__columns)):
            self.__field[row][column] = self.__random.random() < Game.__INITIAL_LIFE_PROBABILITY
        self.__epoch = 0
        self.__is_initialized = True

    def move(self):
        if not self.__is_initialized:
            raise RockartExamplesException("Initialize game first")

        for row, column in itertools.product(range(self.__rows), range(self.__columns)):
            alive_neighbours_number = 0
            for row_offset, column_offset in itertools.product([-1, 0, 1], repeat=2):
                if row_offset == column_offset == 0:
                    continue

                neighbour_row = row + row_offset
                neighbour_column = column + column_offset
                is_neighbour_internal = \
                    0 <= neighbour_row < self.__rows \
                    and 0 <= neighbour_column < self.__columns
                if is_neighbour_internal:
                    is_neighbour_alive = self.__field[neighbour_row][neighbour_column]
                else:
                    is_neighbour_alive = self.__random.random() < Game.__NEIGHBOUR_LIFE_PROBABILITY

                if is_neighbour_alive:
                    alive_neighbours_number += 1

            is_alive = self.__field[row][column]
            if is_alive:
                will_live = alive_neighbours_number in {2, 3}
            else:
                will_live = alive_neighbours_number == 3
            self.__hidden_field[row][column] = will_live
        self.__field, self.__hidden_field = self.__hidden_field, self.__field
        self.__epoch += 1

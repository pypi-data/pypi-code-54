#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from __future__ import annotations

from abc import ABC

import anpy.program
import anpy.utils


class BatchDecoderBuilder(anpy.program.ProgramBuilder, ABC):
    """
    Decoded multiple runs in batch
    """

    def __init__(self) -> None:
        super(BatchDecoderBuilder, self).__init__()
        self._program = anpy.program.Program()

    def reset(self) -> None:
        self._program = anpy.program.Program()

    @property
    def program(self) -> anpy.program.Program:
        program = self._program
        self.reset()
        return program

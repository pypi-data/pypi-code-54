import unittest
from dataclasses import dataclass
from typing import Optional, Dict

from pywood.decorators import event, no_events
from pywood.machine import Machine
from pywood.eventlib import *
from pywood.states import BaseState
from pywood.updates.generate import get_random_update, update_w_random_update_text


@dataclass
class Rec:
    name: Optional[str]
    age: Optional[int]
    state: Optional[str]


class StartState(BaseState):

    @event(IncomingIntNumber)
    def handle_int(self):
        pass

    @no_events
    def foo(self):
        pass


class NameEntered(BaseState):

    @event(IncomingIntNumber)
    def handle_incoming_int_number(self):
        pass


class TestFull(unittest.TestCase):

    def test_abc(self):
        token = 'TOKEN'

        rec1 = Rec('Dzmitry Maliuzhenets', 35, 'AgeEntered')
        rec2 = Rec('Guido Van Rossum', None, 'NameEntered')
        rec3 = Rec(None, None, 'StartState')

        chats = {
            123123123123: rec1,
            234234234234: rec2,
            345345345345: rec3
        }

        def current_state_getter(update) -> str:
            chat_id = update.message.chat.id
            rec = chats.setdefault(chat_id, Rec(None, None, 'StartState'))
            return rec.state


        update_with_text = get_random_update(exclude_chat_ids=[123123123123,
                                                     234234234234,
                                                     345345345345],
                                             funcs=[update_w_random_update_text])

        fsm = Machine(current_state_getter=current_state_getter,
                    states=[StartState, NameEntered], token=token)

        fsm.process(update_with_text)









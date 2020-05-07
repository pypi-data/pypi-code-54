from functools import partial
from typing import Optional, Dict, Any, Callable, List, Type

import telegrambotapiwrapper

from pywood._conversation import Conversation
from pywood.pooling import listen
from pywood.states import BaseState


class Bot:

    def __init__(self,
                 token: str,
                 conversation_states,
                 conversation_state_getter,
                 api_provider_cls=telegrambotapiwrapper.Api,
                 state_attrs: Optional[dict] = None
                 ):
        self.token = token
        self.states = conversation_states
        self.getter = conversation_state_getter
        self.api_provider_cls = api_provider_cls
        self.state_attrs = state_attrs

    def start_pooling(self):
        bot_api = self.api_provider_cls(self.token)
        if self.state_attrs is not None:
            state_attrs_copy = self.state_attrs.copy()
            state_attrs_copy['bot_api'] = bot_api
            handler = partial(handle_update,
                              self.states,
                              self.getter,
                              state_attrs_copy)
        else:
            handler = partial(handle_update,
                              self.states,
                              self.getter,
                              {'bot_api': bot_api})

        listen(self.token,
               handler,
               process_existing=False)

    def handle_update(self, update):
        bot_api = self.api_provider_cls(self.token)
        if self.state_attrs is not None:
            state_attrs_copy = self.state_attrs.copy()
            state_attrs_copy['bot_api'] = bot_api
            handle_update(update,
                          self.states,
                          self.getter,
                          state_attrs_copy)
        else:
            handle_update(update,
                          self.states,
                          self.getter,
                          {'bot_api': bot_api})


def handle_update(update,
                  states: List[Type[BaseState]],
                  conversation_state_getter: Callable,
                  state_attrs: Optional[Dict[str, Any]] = None,
                  ):
    """

    :param update: обновление
    :type update: объект, определяющий объект `Update <https://core.telegram.org/bots/api#update>`_

    :param states: список классов состояний
    :type states: список классов, наследующих от BaseState (List[Type[BaseState]])

    :param conversation_state_getter: callable, принимающее как аргумент `update`,
        и возвращающее

        - строку, содержащую название класса текущего состояния
        - сам класс текущего состояния
        - кортеж, содержащий первым своим элементом название класса текущего
          состояния и вторым элементом дополнительную информацию, которая будет
          добавлена в аргумент `context` обработчиков

    :type conversation_state_getter: callable

    :param state_attrs: (optional) словарь, содержащий аттрибуты, которые будут
        добавлены к экземпляру класса состояния
    :type state_attrs: Dict[str, Any]

    :raises StateDoesNotExistError: выбрасывается, если conversation_state_getter
        возвращает не строку, класс состояния или кортеж

    :return:
    """
    conversation = Conversation(
        conversation_state_getter=conversation_state_getter,
        states=states)
    conversation.process(update=update, state_attrs=state_attrs)

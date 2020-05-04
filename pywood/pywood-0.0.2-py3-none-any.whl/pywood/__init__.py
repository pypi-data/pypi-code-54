from typing import Optional, Dict, Any, Callable, List, Type

from pywood._machine import Machine
from pywood.states import BaseState


def handle_update(update,
                  states: List[Type[BaseState]],
                  current_state_getter: Callable,
                  state_attrs: Optional[Dict[str, Any]] = None,
                  ):
    """

    :param update: обновление
    :type update: объект, определяющий объект `Update <https://core.telegram.org/bots/api#update>`_

    :param states: список классов состояний
    :type states: список классов, наследующих от BaseState (List[Type[BaseState]])

    :param current_state_getter: callable, принимающее как аргумент `update`,
        и возвращающее

        - строку, содержащую название класса текущего состояния
        - сам класс текущего состояния
        - кортеж, содержащий первым своим элементом название класса текущего
          состояния и вторым элементом дополнительную информацию, которая будет
          добавлена в аргумент `context` обработчиков

    :type current_state_getter: callable

    :param state_attrs: (optional) словарь, содержащий аттрибуты, которые будут
        добавлены к экземпляру класса состояния
    :type state_attrs: Dict[str, Any]

    :raises StateDoesNotExistError: выбрасывается, если current_state_getter
        возвращает не строку, класс состояния или кортеж

    :return:
    """
    machine = Machine(current_state_getter=current_state_getter,
                      states=states)
    machine.process(update=update, state_attrs=state_attrs)

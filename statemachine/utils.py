from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, List, Tuple
import inspect

from .exceptions import *


def is_state_handler(handler: Callable) -> bool:
    return inspect.ismethod(handler) and getattr(handler, 'type', None) is State


def is_initial_state(state_metadata: Dict[str, Any]) -> bool:
    return state_metadata.get('_initial')


def get_state_handlers(state_machine: 'StateMachine') -> List[Tuple[Any]]:
    return inspect.getmembers(state_machine, predicate=is_state_handler)


def get_state_handler_by_metadata(state_machine: 'StateMachine', handler_metadata: Dict[str, Any]) -> Callable:
    state_handlers = filter(lambda handler: handler[0] == handler_metadata.get('_name'), get_state_handlers(state_machine))

    try:
        return next(state_handlers)[-1]
    except StopIteration as exception:
        return None


def get_current_state_handler(state_machine: 'StateMachine') -> Callable:
    return get_state_handler_by_metadata(state_machine, state_machine.current_state)


@dataclass
class Binder:
    state: str
    validator: Callable


class Bind:
    def __init__(self, binders: List[Binder]):
        self.binders = binders

    def __call__(self, state_handler_action: Callable):
        @wraps(state_handler_action)
        def wrapper(sm: 'StateMachine', *args, **kwargs):
            result = state_handler_action(sm, *args, **kwargs)

            try:
                destination_state = next(filter(lambda binder: binder.validator(*result), self.binders)).state
                sm.current_state = inspect.getmembers(sm, predicate=lambda member: inspect.ismethod(member) and member.__name__ == destination_state)[0]
                for s in sm.states_metadata:
                    if s.get('_name') == sm.current_state[0]:
                        sm.current_state = s
                        break
                return result
            except StopIteration as exception:
                destination_state = None
                raise StateBinderNotFoundException(sm.current_state.get('_name'))

        return wrapper


class State:
    def __init__(self, name: str, initial: bool = False, finite: bool = False):
        self.name = name
        self.initial = initial
        self.finite = finite

    def __call__(self, state_handler_action: Callable):
        @wraps(state_handler_action)
        def wrapper(state_machine: 'StateMachine', *args, **kwargs):
            return state_handler_action(state_machine, *args, **kwargs)

        wrapper.type = State
        wrapper.metadata = {
            '_name': self.name,
            '_initial': self.initial,
            '_finite': self.finite
        }

        return wrapper

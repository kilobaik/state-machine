import inspect
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, List, Any
from statemachine.exceptions import *
from statemachine.utils import Utils


@dataclass
class StateMetadata:
    name: str = field(metadata={'description': 'The name of the state.'})
    initial: bool = field(default=False, metadata={'description': 'Initial state flag.'})
    finite: bool = field(default=False, metadata={'description': 'Finite state flag.'})


@dataclass
class Binder:
    target_state: str = field(metadata={'description': 'The name of the target_state which should be bound.'})
    validator: Callable = field(metadata={'description': 'The validator of the target state.'})


@dataclass
class Bind:
    binders: List[Binder] = field(default_factory=list, metadata={'description': 'A list of states\' binders.'})

    def __call__(self, state_handler_action: Callable):
        @wraps(state_handler_action)
        def wrapper(state_machine: 'StateMachine', *args, **kwargs):
            result = state_handler_action(state_machine, *args, **kwargs)
            valid_binders = tuple(filter(lambda binder: binder.validator(*result), self.binders))

            if len(valid_binders) == 0:
                raise NoValidBinderFound(state_handler_action.metadata)
            elif len(valid_binders) > 1:
                raise MultipleValidBindersFound(state_handler_action.metadata, valid_binders)
            else:
                valid_binder = valid_binders[0]
                state_machine.current_state = valid_binder.target_state
                return result

        return wrapper


@dataclass
class State:
    name: str = field(metadata={'description': 'The name of the state.'})
    initial: bool = field(default=False, metadata={'description': 'Initial state flag.'})
    finite: bool = field(default=False, metadata={'description': 'Finite state flag.'})

    def __call__(self, state_handler_action: Callable):
        @wraps(state_handler_action)
        def wrapper(state_machine: 'StateMachine', *args, **kwargs):
            return state_handler_action(state_machine, *args, **kwargs)

        wrapper.type = 'state'
        wrapper.metadata = StateMetadata(name=self.name, initial=self.initial, finite=self.finite)

        return wrapper


class StateMachine:
    def __init__(self):
        self.states_metadata, self.current_state = [], None
        states_handlers = inspect.getmembers(self, predicate=Utils.is_state_handler)

        for handler_name, handler_action in states_handlers:
            handler_metadata: StateMetadata = handler_action.metadata
            if handler_metadata in states_handlers:
                raise StateConflictException(handler_name, handler_metadata)

            if handler_metadata.initial:
                if self.current_state is None:
                    self.current_state = handler_metadata.name
                else:
                    raise MultipleInitialStateFound(self.current_state, handler_metadata.name)

            self.states_metadata.append(handler_metadata)

            if self.current_state is None:
                raise NoInitialStateFound()

        self.__initial_state = self.current_state

    def current(self) -> Tuple[Any]:
        state_metadata = Utils.find_current_state_metadata(self)
        state_handler = inspect.getmembers(self, predicate=Utils.find_state_handler(state_metadata))[0][1]

        return state_metadata, state_handler

    def apply(self, *args) -> Any:
        self.current_state = self.__initial_state
        state_metadata, state_handler = self.current()

        while not state_metadata.finite:
            args = state_handler(*args)
            state_metadata, state_handler = self.current()

        return state_handler(*args)

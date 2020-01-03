import inspect
from typing import Callable
from statemachine.exceptions import CurrentStateNotFound


class Utils:
    @staticmethod
    def is_state_handler(handler: Callable):
        return inspect.ismethod(handler) and getattr(handler, 'type', None) == 'state'

    @staticmethod
    def find_state_handler(state_metadata: 'StateMetadata') -> Callable:
        def finder(handler: Callable) -> bool:
            return Utils.is_state_handler(handler) and handler.metadata == state_metadata
        return finder

    @staticmethod
    def find_current_state_metadata(state_machine: 'StateMachine') -> 'StateMetadata':
        states_metadata = filter(lambda _state_metadata: _state_metadata.name == state_machine.current_state,
                                 state_machine.states_metadata)
        try:
            return next(states_metadata)
        except StopIteration as exception:
            raise CurrentStateNotFound(state_machine.current_state)

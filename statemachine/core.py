from typing import Dict, Any, List
from .exceptions import StateConflictException, NoInitialStateFoundException
from .utils import get_state_handlers, is_initial_state, get_state_handler_by_metadata, get_current_state_handler


class StateMachine:
    def __init__(self):
        self.states_metadata = self.__manipulate_state_handlers()
        self.current_state = self.get_initial_state()

    def __manipulate_state_handlers(self) -> List[Dict[str, Any]]:
        states = []
        for handler_name, handler_action in get_state_handlers(self):
            if handler_name != handler_action.metadata.get('_name'):
                raise StateConflictException(handler_name, handler_action.metadata)
            states.append(handler_action.metadata)
        return states

    def get_initial_state(self) -> Dict[str, Any]:
        try:
            return next(filter(is_initial_state, self.states_metadata))
        except StopIteration as exception:
            raise NoInitialStateFoundException(self.states_metadata)

    def apply(self, *data) -> Any:
        while not self.current_state.get('_finite'):
            handler = get_current_state_handler(self)
            data = handler(*data)

        handler = get_current_state_handler(self)
        return handler(*data)

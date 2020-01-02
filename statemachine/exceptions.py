from typing import Any, Dict


class NoInitialStateFoundException(Exception):
    def __init__(self, states: Dict[str, Dict[str, Any]]):
        self.args = (f'No start state found in states {states}', )


class StateConflictException(Exception):
    def __init__(self, state_handler_name: str, state_metadata: Dict[str, Any]):
        self.args = (f'State\'s handler {state_handler_name} does not match state metadata {state_metadata}',)


class StateNotFoundException(Exception):
    def __init__(self, state_name: str):
        self.args = (f'State {state_name} is not defined', )


class StateBinderNotFoundException(Exception):
    def __init__(self, state_name: str):
        self.args = (f'State\'s binder for {state_name} is not defined', )

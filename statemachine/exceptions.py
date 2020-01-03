from typing import Tuple


class NoValidBinderFound(Exception):
    def __init__(self, state_metadata: 'StateMetadata'):
        self.args(f'No valid binder found for state="{state_metadata.name}".', )


class MultipleValidBindersFound(Exception):
    def __init__(self, state_metadata: 'StateMetadata', valid_binders: Tuple['Binder']):
        self.args = (f'Multiple valid binders found for state="{state_metadata.name}", valid_binders={valid_binders}.', )


class StateConflictException(Exception):
    def __init__(self, state_handler_name: str, state_metadata: 'StateMetadata'):
        self.args = (f'State\'s handler {state_handler_name} does not match state metadata {state_metadata}.', )


class MultipleInitialStateFound(Exception):
    def __init__(self, first_initial_state: str, second_initial_state: str):
        self.args = (f'Multiple initial states found first={first_initial_state}, second={second_initial_state}.', )


class NoInitialStateFound(Exception):
    def __init__(self):
        self.args = ('No initial state found.', )


class CurrentStateNotFound(Exception):
    def __init__(self, current_state: str):
        self.args = (f'No valid current state {current_state}', )

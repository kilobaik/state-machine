from statemachine.core import *
from statemachine.utils import *


class SM(StateMachine):
    def __init__(self, *args, **kwargs):
        super(SM, self).__init__(*args, **kwargs)

    @State(name='s0', initial=True)
    @Bind([
        Binder(state='s1', validator=lambda n, m: 0 < m),
        Binder(state='s2', validator=lambda n, m: m < 0),
    ])
    def s0(self, n: int, m: int):
        print(f's0(n={n}, m={m})')
        return n, m

    @State(name='s1')
    @Bind([
        Binder(state='s1', validator=lambda n, m: 0 < m),
        Binder(state='s3', validator=lambda n, m: m == 0)
    ])
    def s1(self, n: int, m: int):
        print(f's1(n={n}, m={m})')
        return n + 1, m - 1

    @State(name='s2')
    @Bind([
        Binder(state='s2', validator=lambda n, m: m < 0),
        Binder(state='s3', validator=lambda n, m: m == 0)
    ])
    def s2(self, n: int, m: int):
        print(f's2(n={n}, m={m})')
        return n - 1, m + 1

    @State(name='s3', finite=True)
    def s3(self, n: int, m: int):
        print(f's3(n={n}, m={m})')
        return n - 1


sm = SM()
print(sm.apply(3, -5))

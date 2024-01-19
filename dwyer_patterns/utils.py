from bppy import BEvent, EventSet
import itertools


class Assignment(BEvent):
    def __init__(self, kwargs):
        super().__init__("_".join([str(k) + ("T" if v else "F") for k, v in kwargs.items()]))
        self.__dict__.update(kwargs)


variables_names = ["q", "p", "r", "s", "t", "z"]
event_list = [Assignment({k: v for k, v in zip(variables_names, values)}) for values in itertools.product([True, False], repeat=len(variables_names))]

q = EventSet(lambda e: "qT" in e.name)
p = EventSet(lambda e: "pT" in e.name)
r = EventSet(lambda e: "rT" in e.name)
s = EventSet(lambda e: "sT" in e.name)
t = EventSet(lambda e: "tT" in e.name)
z = EventSet(lambda e: "zT" in e.name)
non_det = EventSet(lambda e: "dT" in e.name)


class Not(EventSet):
    def __init__(self, event_set):
        super().__init__(lambda e: e not in event_set)


class And(EventSet):
    def __init__(self, *args):
        super().__init__(lambda e: all(e in event_set for event_set in args))


class Or(EventSet):
    def __init__(self, *args):
        super().__init__(lambda e: any(e in event_set for event_set in args))


class true(EventSet):
    def __init__(self):
        super().__init__(lambda e: True)

class false(EventSet):
    def __init__(self):
        super().__init__(lambda e: False)

def non_deterministic(e):
    return e in non_det

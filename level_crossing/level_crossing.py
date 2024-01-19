from bppy import *
from bppy.utils.dfs import DFSBProgram
import graphviz


class Sensor(BEvent):
    def __init__(self, railway, type):
        super().__init__(str(type) + str(railway))
        self.railway = railway
        self.type = type

    def __str__(self):
        return str(self.type) + str(self.railway)


class Approaching(Sensor):
    def __init__(self, railway):
        super().__init__(railway, "Ap")


class Entering(Sensor):
    def __init__(self, railway):
        super().__init__(railway, "En")


class Leaving(Sensor):
    def __init__(self, railway):
        super().__init__(railway, "Le")


class Lower(BEvent):
    def __init__(self):
        super().__init__("Lower")

    def __str__(self):
        return "Lower"


class Raise(BEvent):
    def __init__(self):
        super().__init__("Raise")

    def __str__(self):
        return "Raise"


any_approaching = EventSet(lambda e: isinstance(e, Approaching))
any_entering = EventSet(lambda e: isinstance(e, Entering))


@b_thread  # R1: Railway sensors
def req_1(railway):
    while True:
        yield {waitFor: Approaching(railway)}
        yield {request: Entering(railway),
               block: Approaching(railway)}
        yield {request: Leaving(railway),
               block: Approaching(railway)}


@b_thread  # R2: Barriers dynamics
def req_2():
    while True:
        yield {waitFor: any_approaching}
        yield {request: Lower()}
        yield {request: Raise()}


@b_thread  # R3: No entering while barriers are up
def req_3():
    while True:
        yield {waitFor: Lower(), block: any_entering}
        yield {waitFor: Raise()}


@b_thread  # R4: No raising while a train is inside
def req_4(railway):
    while True:
        yield {waitFor: Approaching(railway)}
        yield {waitFor: Leaving(railway), block: Raise()}


@b_thread  # R5: Passenger trains
def req_5():
    while True:
        yield {request: Approaching("Pas")}


@b_thread  # R6: Freight trains
def req_6():
    for i in range(3):
        yield {request: Approaching("Fre"), mustFinish: True}


@b_thread  # R7: Maintenance trains
def req_7():
    for i in range(3):
        yield {request: Approaching("Mai")}


@b_thread
def req_8():
    while True:
        yield {waitFor: Approaching("Fre")}
        yield {waitFor: Approaching("Mai"),
               block: Approaching("Fre")}


def bprogram_gen():
    bthreads = [req_6(), req_1("Pas"), req_1("Fre"), req_1("Mai"),
                req_2(), req_3(), req_4("Pas"), req_4("Fre"),
                req_4("Mai"), req_5(),
                req_7(), req_8()]
    return BProgram(bthreads=bthreads,
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())


def print_graph(states):
    before = 0
    after = 0
    for i, s in enumerate(states):
        if not s.nodes[0].data.get(mustFinish, False):
            s.color = "green"
            after += 1
        else :
            s.color = "red"
    while before != after:
        print(before, after)
        before = after
        for i, s in enumerate(states):
            if s.color == "green":
                continue
            for e, s_new in s.transitions.items():
                if states[states.index(s_new)].color == "green":
                    s.color = "green"
                    after += 1
                    break

    g = graphviz.Digraph()
    g.attr(rankdir='LR')
    for i, s in enumerate(states):
        s.graph_id = str(i)
        g.node(str(i), shape='doublecircle' if i == 0 else 'circle', color=s.color, fillcolor=s.color, style="filled")
    for i, s in enumerate(states):
        for e, s_new in s.transitions.items():
            g.edge(str(i), states[states.index(s_new)].graph_id, label=str(e))
    g.render(directory="output", filename="level_crossing_big")
    print(g)




dfs = DFSBProgram(bprogram_gen)
init, visited = dfs.run()
print("Number of states:", len(visited))
print_graph(visited)

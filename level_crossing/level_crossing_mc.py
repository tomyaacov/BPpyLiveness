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
    if railway == "Fre":
        while True:
            yield {waitFor: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}
            yield {request: Entering(railway),
                   block: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}
            yield {request: Leaving(railway),
                   block: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}
    else:
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
    if railway == "Fre":
        while True:
            yield {waitFor: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}
            yield {waitFor: Leaving(railway), block: Raise()}
    else:
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
        yield {request: Approaching("Fre"+str(i)), mustFinish: True}


@b_thread  # R7: Maintenance trains
def req_7():
    for i in range(3):
        yield {request: Approaching("Mai")}


@b_thread
def req_8():
    while True:
        yield {waitFor: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}
        yield {waitFor: Approaching("Mai"),
               block: [Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")]}

# @b_thread
# def avoid_passsenger_starvation():
#     while True:
#         yield {waitFor: Approaching("Pas")}
#         yield {waitFor: any_approaching,
#                block: Approaching("Pas")}



@b_thread
def fix_scheduling_issues():
    for i in range(3):
        block_list = []
        e = yield {waitFor: any_approaching}
        if e.name.startswith("Fre"):
            block_list.extend([Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")])
        else:
            block_list.append(e)
        e = yield {waitFor: any_approaching, block: block_list}
        if e.name.startswith("Fre"):
            block_list.extend([Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2")])
        else:
            block_list.append(e)
        yield {waitFor: any_approaching, block: block_list}

def bprogram_gen():
    bthreads = [req_6(), req_1("Pas"), req_1("Fre"), req_1("Mai"),
                req_2(), req_3(), req_4("Pas"), req_4("Fre"),
                req_4("Mai"), req_5(),
                req_7(), req_8(),
                fix_scheduling_issues()
                ]
    return BProgram(bthreads=bthreads,
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())


def model_check():
    from bppy.analysis.symbolic_bprogram_verifier import SymbolicBProgramVerifier
    all_events = [Approaching("Pas"), Approaching("Fre0"), Approaching("Fre1"), Approaching("Fre2"), Approaching("Mai"),
                  Entering("Pas"), Entering("Fre"), Entering("Mai"),
                  Leaving("Pas"), Leaving("Fre"), Leaving("Mai"),
                  Lower(), Raise()]
    verifier = SymbolicBProgramVerifier(bprogram_gen, all_events)
    result, explanation_str = verifier.verify("F event = ApFre2", find_counterexample=True)
    if result:
        print("OK")
    else:
        print("Violation Found")
        print("Counterexample:")
        print(explanation_str)

model_check()




import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread

state = "state"
params = {
    "n": None,
    "k": None
}


def add_a():
    for i in range(0, params["n"]):
        yield {request: bp.BEvent("H"), state: i, mustFinish: True}
    while True:
        yield {state: params["n"], mustFinish: False}


def add_b():
    for i in range(0, params["n"]):
        yield {request: bp.BEvent("C"), state: i, mustFinish: False}
    while True:
        yield {state: params["n"], mustFinish: False}
    # while True:
    #     yield {request: bp.BEvent("I"), state: params["n"], mustFinish: False}


def control():
    while True:
        for i in range(0, params["k"]):
            e = yield {waitFor: [bp.BEvent("C"), bp.BEvent("H")], state: i, mustFinish: False}
            if e.name == "C":
                break
        if e.name == "H":
            yield {waitFor: bp.BEvent("C"), block: bp.BEvent("H"), state: params["k"], mustFinish: False}


def init_bprogram():
    return bp.BProgram(bthreads=[add_a(), add_b(), control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())

if __name__ == '__main__':
    params["n"] = 3
    init_bprogram().run()

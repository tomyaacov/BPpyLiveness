import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread

state = "state"
params = {
    "n": None,  # number of Cs and Hs
    "k": None,  # block k + 1 Hs in a row
    "m": None  #
}


def add_a():
    for i in range(0, params["n"]):
        yield {request: bp.BEvent("H"), state: i, mustFinish: True}
    while True:
        yield {state: params["n"], mustFinish: False}


def add_b(name):
    for i in range(0, params["n"]):
        yield {request: bp.BEvent("C" + name), state: i, mustFinish: False}
    while True:
        yield {state: params["n"], mustFinish: False}


def control():
    while True:
        for i in range(0, params["k"]):
            e = yield {waitFor: bp.All(), state: i, mustFinish: False}
            if e.name == "C":
                break
        if e.name == "H":
            yield {waitFor: bp.BEvent("C0"), block: bp.BEvent("H"), state: params["k"], mustFinish: False}


def init_bprogram():
    return bp.BProgram(bthreads=[add_a()] + [add_b(str(x)) for x in range(params["m"])] + [control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())


def get_event_list():
    return [bp.BEvent("H")] + [bp.BEvent("C" + str(x)) for x in range(params["m"])]


if __name__ == '__main__':
    params["n"] = 2
    params["k"] = 1
    params["m"] = 3
    init_bprogram().run()

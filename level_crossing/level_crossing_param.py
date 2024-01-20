import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread

state = "state"
params = {
    "n": None,  # number of Cs and Hs
    "k": None,  # block k + 1 Hs in a row
    "m": None  #
}

@bp.thread
def req_6():
    for i in range(0, params["n"]):
        yield bp.sync(request=bp.BEvent("F"), state=i, mustFinish=True)
    while True:
        yield bp.sync(state=params["n"], mustFinish=False)

@bp.thread
def req_7(name):
    for i in range(0, params["n"]):
        yield bp.sync(request=bp.BEvent("M" + name), state=i, mustFinish=False)
    while True:
        yield bp.sync(state=params["n"], mustFinish=False)

@bp.thread
def req_8():
    while True:
        for i in range(0, params["k"]):
            e = yield bp.sync(waitFor=bp.All(), state=i, mustFinish=False)
            if e.name.startswith("M"):
                break
        if e.name == "F":
            e = yield bp.sync(waitFor=bp.BEvent("M0"), block=bp.BEvent("F"), state=params["k"], mustFinish=False)


def init_bprogram():
    return bp.BProgram(bthreads=[req_6()] + [req_7(str(x)) for x in range(params["m"])] + [req_8()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())


def get_event_list():
    return [bp.BEvent("F")] + [bp.BEvent("M" + str(x)) for x in range(params["m"])]


if __name__ == '__main__':
    params["n"] = 2
    params["k"] = 1
    params["m"] = 3
    init_bprogram().run()


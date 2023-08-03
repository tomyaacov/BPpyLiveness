import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread


def data(turtle_location, turtle_orientation, lidar_data):
    return bp.BEvent("data", {"turtle_location": turtle_location,
                              "turtle_orientation": turtle_orientation,
                              "lidar_data": lidar_data})


any_data = bp.EventSet(lambda e: e.name == "data")


def move():
    return bp.BEvent("move")

def rotate():
    return bp.BEvent("rotate")


any_action = bp.EventSet(lambda e: e.name == "move" or e.name == "rotate")

@b_thread
def interleave():
    while True:
        yield {block: any_action, waitFor: any_data}
        yield {block: any_data, waitFor: any_action}


@b_thread
def block_rotate():
    while True:
        yield {waitFor: rotate()}
        yield {block: rotate(), waitFor: move()}
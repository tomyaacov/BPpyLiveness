from dwyer_patterns.symbolic_bprogram_verifier import SymbolicBProgramVerifier
from dwyer_patterns.patterns import *
from bppy.model.bprogram import BProgram
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy


# pattern = pat_0
# spec = "F ( G p)"
# variables_names = ["p", "d"]

# pattern = pat_8
# spec = "G !q | F (q & F p)"
# variables_names = ["q", "p"]


# pattern = pat_10
# spec = "G (!(q & !r) | (!r U (p & !r)))"
# variables_names = ["q", "p", "r"]

# pattern = pat_23  # TODO: not correct
# spec = "G !q | F (q & (s U (!p | s)))"
# variables_names = ["q", "p", "s", "d"]

# pattern = pat_26
# spec = "G (!p | F s)"
# variables_names = ["p", "s"]


# pattern = pat_28
# spec = "G (!q | G (!p | F s))"
# variables_names = ["q", "p", "s"]

# pattern = pat_30
# spec = "G (!(q & !r) | (r V (!p | r | (!r U (!r & s)))))"
# variables_names = ["q", "p", "r", "s"]

# pattern = pat_41 # TODO: not correct
# spec = "G (X (t & F p) | ! (s & X t))"
# variables_names = ["s", "t", "p"]

pattern = pat_46  # TODO: completeness check doesn't work
spec = "G (!p | F (s & X t))"
variables_names = ["p", "s", "t", "d"]

# pattern = pat_48  # TODO: completeness check doesn't work
# spec = "G (!q | G (!p | (s & X t)))"
# variables_names = ["q", "p", "s", "t"]

event_list = [Assignment({k: v for k, v in zip(variables_names, values)}) for values in itertools.product([True, False], repeat=len(variables_names))]

@b_thread
def general():
    while True:
        yield {request: event_list}


def bprogram_generator():
    return BProgram(bthreads=[general(), pattern()],
                    event_selection_strategy=SimpleEventSelectionStrategy())


verifier = SymbolicBProgramVerifier(bprogram_generator, event_list)

assumption = "G ( F must_finish = FALSE )"

if "d" in variables_names:
    non_det_assumption = "G ( F d )"
else:
    non_det_assumption = "TRUE"

result, explanation_str = verifier.verify(spec=f"G ( ( {assumption} ) & ( {non_det_assumption} ) ) -> ( {spec} )", type="BDD", find_counterexample=True,
                                          print_info=False)


if result:
    print("Under assumption specification holds - OK")
else:
    print("Under assumption - Violation Found! Counterexample:")
    print(explanation_str)


result, explanation_str = verifier.verify(spec=f"G ( ! ( {assumption} ) & ( {non_det_assumption} ) ) -> ( ! ( {spec} ) )", type="BDD", find_counterexample=True,
                                          print_info=False)


if result:
    print("If assumption does not hold - specification does not hold - OK")
else:
    print("If assumption does not hold - specification holds - Violation Found! Counterexample:")
    print(explanation_str)

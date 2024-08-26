from ..classes import *
import logging
from typing import List, Dict, Set, Tuple
logger = logging.getLogger(__name__)


class State_Set:
    state: Set[str] = None

    def __init__(self, state=None):
        if state is None:
            state = set()
        self.state = state

    def __str__(self):
        return "|".join(self.state)

    def add(self, tr: str) -> None:
        if tr == "":
            tr = "$"
        self.state.add(tr)

    def update(self, new_set: 'State_Set | None'):
        if new_set is None:
            return
        self.state.update(new_set.state)

    def __bool__(self):
        # for state in self.state:
        #     if state:
        #         return True
        # return False
        return bool(self.state)

    def __len__(self):
        return len(self.state)


def _get_transition_set(transitions: Dict[str, bool]) -> Set[str]:
    return set([char for char, allowed in transitions.items() if allowed])


def _create_basis(atm: Automat, n: int) -> Dict[int, Dict[int, State_Set]]:
    basis: Dict[int, Dict[int, State_Set]] = {}
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            basis[i] = basis.get(i, {})
            if j in atm.state_map[i]:
                basis[i][j] = State_Set(_get_transition_set(atm.state_map[i][j]))
            if i == j:
                basis[i][j] = basis[i].get(j, State_Set())
                basis[i][j].add("")
    return basis

def _rename_states(atm: Automat):
    state_dict: Dict[int, int] = {}
    for new_id, state in enumerate(atm.state_map.keys()):
        state_dict[state] = new_id + 1

    new_state_map: Dict[int, Dict[int, Dict[str, bool]]] = {}
    new_current_set: Set[int] = set()
    new_allowed_set: Set[int] = set()
    new_capture_groups: Dict[int, Set[Tuple[int, int]]] = {}
    for from_id, values in atm.state_map.items():
        new_state_map[state_dict[from_id]] = {}
        for to_id, transitions in values.items():
            new_state_map[state_dict[from_id]][state_dict[to_id]] = atm.state_map[from_id][to_id]
    atm.state_map = new_state_map

    for allowed in atm.allowed_set:
        new_allowed_set.add(state_dict[allowed])
    atm.allowed_set = new_allowed_set

    for current in atm.current_set:
        new_current_set.add(state_dict[current])
    atm.current_set = new_current_set

    for cp_group, cp_tuples in atm.capture_groups.items():
        new_capture_groups[cp_group] = set()
        for cp_tuple in cp_tuples:
            new_capture_groups[cp_group].add((state_dict[cp_tuple[0]], state_dict[cp_tuple[1]]))
    atm.capture_groups = new_capture_groups
    atm.fill_search_capture_map()
    atm.start = state_dict[atm.start]


def re_k_path(atm: Automat) -> str:
    _rename_states(atm)
    n: int = max(atm.state_map.keys())
    # struct is {k: from: to: regex}
    prev_states: Dict[int, Dict[int, State_Set]] = _create_basis(atm, n)
    current_states: Dict[int, Dict[int, State_Set]] = {}
    # induction_states: Dict[int, Dict[int, Dict[int, State_Set]]] = {0: _create_basis(atm, n)}
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            current_states[i] = current_states.get(i, {})
            for j in range(1, n + 1):
                current_states[i][j] = current_states[i].get(j, State_Set())
                current_states[i][j].update(prev_states[i].get(j, None))
                if prev_states[i].get(k, None) and prev_states[k].get(j, None):
                    if str(prev_states[k][k]) != "$":
                        fst = f"(!{prev_states[i][k]})" if len(prev_states[i][k]) > 1 else f"{prev_states[i][k]}"
                        fst = "" if fst == "$" else fst
                        snd = f"(!{prev_states[k][j]})" if len(prev_states[k][j]) > 1 else f"{prev_states[k][j]}"
                        snd = "" if snd == "$" else snd
                        current_states[i][j].add(f"{fst}(!{prev_states[k][k]})*{snd}")
                    else:
                        if str(prev_states[i][k]) == "$":
                            current_states[i][j].update(prev_states[k][j])
                        elif str(prev_states[k][j]) == "$":
                            current_states[i][j].update(prev_states[i][k])
                        else:
                            fst = f"(!{prev_states[i][k]})" if len(prev_states[i][k]) > 1 else f"{prev_states[i][k]}"
                            snd = f"(!{prev_states[k][j]})" if len(prev_states[k][j]) > 1 else f"{prev_states[k][j]}"
                            current_states[i][j].add(f"{fst}{snd}")
        prev_states = current_states
        current_states = {}
    starter = atm.start
    result = "|".join([f"(!{prev_states[starter][allowed]})" for allowed in atm.allowed_set])
    return result
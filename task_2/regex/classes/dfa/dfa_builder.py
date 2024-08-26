import logging
import queue

from ..status import Status
from ..automat import Automat, alphabet
from typing import Set, Dict, List, FrozenSet
from queue import Queue

class _frozen_state_group:
    states: FrozenSet[int] = None
    _group_id: int = 1
    id: int = None

    def __init__(self, states):
        self.states = frozenset(states)
        self.id = _frozen_state_group._group_id
        _frozen_state_group._group_id += 1

def next_state_set(atm: Automat, state_set: FrozenSet[int] | Set[int], condition: str, is_nfa: bool = True) -> Set[int]:
    if type(state_set) == set:
        _state_set = frozenset(state_set)
    visited_states: Set[int] = set()
    def _recursive_func(_atm: Automat, _state_set: FrozenSet[int], _condition: str, _is_nfa: bool = True):
        resulting_set: Set[int] = set()
        for state in _state_set:
            if state not in _atm.state_map:
                logging.error("_next_state_set error, wrong state_set, state doesnt exists")
                raise ValueError("wrong state_set when trying to _next_state_set()")
            from_id: int = state
            for to_id, transitions in _atm.state_map[from_id].items():
                if transitions[_condition]:
                    resulting_set.add(to_id)
            if _is_nfa:
                next_set = resulting_set.difference(visited_states)
                visited_states.update(resulting_set)
                recursive_set = _recursive_func(_atm, frozenset(next_set), _condition)
                if type(recursive_set) is Status:
                    return recursive_set
                resulting_set.update(recursive_set)
        return resulting_set

    return _recursive_func(atm, state_set, condition, is_nfa)


def build_dfa(nfa: Automat) -> Automat | Status:
    dfa: Automat = Automat()
    starting_set: Set[int] | Status = next_state_set(nfa, {nfa.start}, "", True)
    if type(starting_set) is Status:
        return starting_set
    starting_set.add(nfa.start)
    state_queue: Queue[_frozen_state_group] = Queue()
    starting_group = _frozen_state_group(starting_set)
    state_queue.put(starting_group)
    dfa.start = starting_group.id
    group_dict: Dict[FrozenSet[int], int] = {starting_group.states: starting_group.id}

    while not state_queue.empty():
        candidate_group = state_queue.get()
        for char in alphabet:
            char_states: Set[int] | Status = next_state_set(nfa, candidate_group.states, char, True)
            if type(char_states) is Status:
                return char_states
            after_epsilon: Set[int] | Status = next_state_set(nfa, char_states, "", True)
            if type(after_epsilon) is Status:
                return after_epsilon
            char_states.update(after_epsilon)
            current_group = _frozen_state_group(char_states)

            if len(current_group.states) != 0:
                if current_group.states in group_dict:
                    dfa.add_transition(candidate_group.id, group_dict[current_group.states], char)
                else:
                    state_queue.put(current_group)
                    group_dict[current_group.states] = current_group.id
                    dfa.add_transition(candidate_group.id, current_group.id, char)
    for group_set, group_id in group_dict.items():
        for state in group_set:
            if state in nfa.allowed_set:
                dfa.allowed_set.add(group_id)
            if nfa.capture_groups:
                for cp_group, cp_states in nfa.capture_groups.items():
                    if state in cp_states:
                        dfa.add_capture(group_id, cp_group)

    return dfa
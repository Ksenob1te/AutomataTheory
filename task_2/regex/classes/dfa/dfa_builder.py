import logging
import queue

from ..status import Status
from ..automat import Automat, alphabet
from typing import Set, Dict, List, FrozenSet, Tuple
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

    states_groups_id: Dict[int, Set[int]] = {}
    for group_set, group_id in group_dict.items():
        for state in group_set:
            states_groups_id[state] = states_groups_id.get(state, set())
            states_groups_id[state].add(group_id)

    # group_root: Dict[int, int] = {}
    # for group_set, group_id in group_dict.items():
    #     for state in group_set:
    #         is_state: bool = True
    #         for from_id, values in nfa.state_map.items():
    #             for to_id, transition in values.items():
    #                 if to_id == state and [x for x in states_groups_id[state] if x in states_groups_id[from_id] and x == group_id]:
    #                     is_state = False
    #                     break
    #             if not is_state:
    #                 break
    #         if is_state:
    #             group_root[group_id] = state
    #
    # achievable_in_group: Dict[int, Dict[int, Set[int]]] = {}
    # def _find_all_capture(_state, _capture_id, _cp_states, _group_id) -> Set[int]:
    #     _achievable: Set[int] = set()
    #     def __recursive(__state):
    #         for _cp_state in _cp_states:
    #             if _cp_state[0] == __state:
    #                 if _cp_state[1] not in _achievable and _group_id in states_groups_id[_cp_state[1]]:
    #                     _achievable.add(_cp_state[1])
    #                     __recursive(_cp_state[1])
    #     __recursive(_state)
    #     return _achievable
    #
    # for group_set, group_id in group_dict.items():
    #     achievable_in_group[group_id] = achievable_in_group.get(group_id, {})
    #     for cp_group, cp_states in nfa.capture_groups.items():
    #         achievable_in_group[group_id][cp_group] = _find_all_capture(group_root[group_id], cp_group, cp_states, group_id)


    def _check_group_cycle(_state: int, _group_set: FrozenSet[int]) -> bool:
        _achievable: Set[int] = set()
        def __recursive(__state):
            for __from_id, __values in nfa.state_map.items():
                if __from_id != __state:
                    continue
                for __to_id, __transitions in __values.items():
                    if __to_id not in _group_set:
                        continue
                    if __to_id in _achievable:
                        return True
                    _achievable.add(__to_id)
                    status = __recursive(__to_id)
                    if status:
                        return True
        return __recursive(_state)


    for group_set, group_id in group_dict.items():
        for state in group_set:
            if state in nfa.allowed_set:
                dfa.allowed_set.add(group_id)
            if not nfa.capture_groups:
                continue
            for cp_group, cp_states in nfa.capture_groups.items():
                for cp_state in cp_states:
                    if state == cp_state[0]:
                        searching_groups = states_groups_id[cp_state[1]].copy()
                        transitions = nfa.state_map.get(cp_state[0], {}).get(cp_state[1], {})
                        if not transitions:
                            continue
                        if transitions.get("", False):
                            if _check_group_cycle(state, group_set):
                                searching_groups = [group_id]
                            else:
                                searching_groups = []
                        elif group_id in searching_groups:
                            searching_groups.remove(group_id)
                        for group in searching_groups:
                            dfa.add_capture((group_id, group), cp_group)
                            # dfa.add_capture((group_id, group_id), cp_group)

                    # if cp_state[1] == state:
                    #     dfa.add_capture((states_groups_id[cp_state[0]], group_id), cp_group)

    return dfa
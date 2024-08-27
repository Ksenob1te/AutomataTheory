import logging
import queue

from ..automat import Automat, alphabet
from typing import Set, Dict, List, FrozenSet, Tuple
from queue import Queue
from enum import Enum

class _state_group:
    states: Set[int] = None
    _group_id: int = 1
    id: int = None

    def __init__(self, states: Set[int]):
        self.states = states
        self.id = _state_group._group_id
        _state_group._group_id += 1


class GROUP_STATUS(Enum):
    UNDEF = 0
    SELF = 1
    DISTINGUISH = 2
    SELF_DONE = 3

def _split_groups(dfa: Automat) -> List[_state_group]:
    unbound_groups: List[_state_group] = []
    states_capture_groups: Dict[int, Set[int]] = {}
    for capture_group, states in dfa.capture_groups.items():
        for state in states:
            states_capture_groups[state[0]] = states_capture_groups.get(state[0], set())
            states_capture_groups[state[0]].add(capture_group)

    capture_groups_states: Dict[FrozenSet[int], Set[int]] = {}
    for state, capture_groups_set in states_capture_groups.items():
        _fr_set = frozenset(capture_groups_set)
        capture_groups_states[_fr_set] = capture_groups_states.get(_fr_set, set())
        capture_groups_states[_fr_set].add(state)

    for capture_groups_set, states in capture_groups_states.items():
        allowed_states: Set[int] = set()
        non_allowed_states: Set[int] = set()
        for state in states:
            if state in dfa.allowed_set:
                allowed_states.add(state)
            else:
                non_allowed_states.add(state)
        if allowed_states:
            unbound_groups.append(_state_group(allowed_states))
        if non_allowed_states:
            unbound_groups.append(_state_group(non_allowed_states))

    non_captured_allowed: Set[int] = set()
    non_captured_non_allowed: Set[int] = set()
    for state, value in dfa.state_map.items():
        is_captured: bool = False
        for capture_index, state_set in dfa.capture_groups.items():
            for state_tuple in state_set:
                if state == state_tuple[0]:
                    is_captured = True
        if not is_captured:
            if state in dfa.allowed_set:
                non_captured_allowed.add(state)
            else:
                non_captured_non_allowed.add(state)
    if non_captured_allowed:
        unbound_groups.append(_state_group(non_captured_allowed))
    if non_captured_non_allowed:
        unbound_groups.append(_state_group(non_captured_non_allowed))
    return unbound_groups


def _analyse_group(dfa: Automat, unbound_groups: List[_state_group]) -> List[_state_group]:
    change_flag: bool = True
    while change_flag:
        change_flag = False
        for i in range(0, len(unbound_groups)):
            distinguish_dict: Dict[int, Dict[int, GROUP_STATUS]] = {}
            for state_1 in unbound_groups[i].states:
                distinguish_dict[state_1] = distinguish_dict.get(state_1, {})
                for state_2 in unbound_groups[i].states:
                    if state_1 == state_2:
                        distinguish_dict[state_1][state_2] = GROUP_STATUS.SELF
                    else:
                        distinguish_dict[state_1][state_2] = GROUP_STATUS.UNDEF

            for state_1 in unbound_groups[i].states:
                for state_2 in unbound_groups[i].states:
                    if distinguish_dict[state_1][state_2] != GROUP_STATUS.UNDEF:
                        continue

                    for char in alphabet:
                        dest_1: int | None = None
                        for to_id, transition in dfa.state_map[state_1].items():
                            if transition[char]:
                                dest_1 = to_id
                                break
                        dest_2: int | None = None
                        for to_id, transition in dfa.state_map[state_2].items():
                            if transition[char]:
                                dest_2 = to_id
                                break
                        if dest_1 is None and dest_2 is None:
                            continue
                        elif dest_1 is None or dest_2 is None:
                            distinguish_dict[state_1][state_2] = GROUP_STATUS.DISTINGUISH
                            distinguish_dict[state_2][state_1] = GROUP_STATUS.DISTINGUISH
                        else:
                            for group in unbound_groups:
                                if (dest_1 in group.states and dest_2 not in group.states) or \
                                    (dest_1 not in group.states and dest_1 in group.states):
                                    distinguish_dict[state_1][state_2] = GROUP_STATUS.DISTINGUISH
                                    distinguish_dict[state_2][state_1] = GROUP_STATUS.DISTINGUISH
                                    break
            for state_1, dist_value in distinguish_dict.items():
                if dist_value[state_1] == GROUP_STATUS.SELF_DONE:
                    continue
                still_good_set: Set[int] = {state_1}
                for state_2, status in dist_value.items():
                    if status is GROUP_STATUS.UNDEF:
                        still_good_set.add(state_2)

                if still_good_set == unbound_groups[i].states:
                    break
                else:
                    change_flag = True
                    unbound_groups.append(_state_group(still_good_set))
                    for good_state in still_good_set:
                        distinguish_dict[good_state][good_state] = GROUP_STATUS.SELF_DONE
                        unbound_groups[i].states.remove(good_state)
    return unbound_groups


def _recreate_dfa(dfa: Automat, unbound_groups: List[_state_group]) -> Automat:
    min_dfa: Automat = Automat()
    state_group_id: Dict[int, int] = {}

    for group in unbound_groups:
        for state in group.states:
            state_group_id[state] = group.id

    for group in unbound_groups:
        for state in group.states:
            if state in dfa.allowed_set:
                min_dfa.allowed_set.add(group.id)
            if state == dfa.start:
                min_dfa.start = group.id
            if not dfa.capture_groups:
                continue
            for cp_group_id, cp_states in dfa.capture_groups.items():
                for cp_state in cp_states:
                    if cp_state[0] == state:
                        min_dfa.add_capture((group.id, state_group_id[cp_state[1]]), cp_group_id)

    for group_1 in unbound_groups:
        for from_id in group_1.states:
            for to_id, transitions in dfa.state_map[from_id].items():
                for transition, condition in transitions.items():
                    for group_2 in unbound_groups:
                        if condition and to_id in group_2.states:
                            min_dfa.add_transition(group_1.id, group_2.id, transition)
    return min_dfa


def _clear_capture_groups(dfa: Automat):
    new_capture_group: Dict[int, Set[Tuple[int, int]]] = {}
    for cp_group_id, cp_group_tuples in dfa.capture_groups.items():
        new_capture_group[cp_group_id] = new_capture_group.get(cp_group_id, set())
        for cp_group_tuple in cp_group_tuples:
            if cp_group_tuple[1] in dfa.state_map[cp_group_tuple[0]]:
                new_capture_group[cp_group_id].add(cp_group_tuple)
    dfa.capture_groups = new_capture_group


def dfa_minimizer(dfa: Automat) -> Automat:
    """
    Minimize the DFA
    :param dfa: Automat
    :return: Minimized automat
    """
    unbound_groups = _split_groups(dfa)
    unbound_groups = _analyse_group(dfa, unbound_groups)
    dfa = _recreate_dfa(dfa, unbound_groups)
    _clear_capture_groups(dfa)
    return dfa





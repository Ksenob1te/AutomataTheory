from ..classes import *
from ..methods import re_compile
import logging
from typing import List, Dict, Set, Tuple
from .product import product_dfa
from .k_path import re_k_path
logger = logging.getLogger(__name__)

def _reverse_tuple(target: Tuple[int, int]) -> Tuple[int, int]:
    return target[1], target[0]

def inverse_re(atm: Automat | str) -> Automat:
    """
    Inverse the regular expression so that it will accept reverse of the original strings
    :param atm: Automat | str
    :return: Automat
    """
    if type(atm) == Automat:
        atm = re_k_path(atm)
    atm = build_ast(atm)
    atm = build_nfa(atm, 1)
    new_state_map: Dict[int, Dict[int, Dict[str, bool]]] = {}
    new_capture_groups: Dict[int, Set[Tuple[int, int]]] = {}
    for from_id, values in atm.state_map.items():
        new_state_map[from_id] = new_state_map.get(from_id, {})
        for to_id, transitions in values.items():
            new_state_map[to_id] = new_state_map.get(to_id, {})
            new_state_map[to_id][from_id] = atm.state_map[from_id][to_id]
    atm.state_map = new_state_map

    for cp_group, cp_tuples in atm.capture_groups.items():
        new_capture_groups[cp_group] = set()
        for cp_tuple in cp_tuples:
            new_capture_groups[cp_group].add(_reverse_tuple(cp_tuple))
    atm.capture_groups = new_capture_groups
    atm.start, atm.end = atm.end, atm.start
    atm.allowed_set = {atm.end}
    atm = build_dfa(atm)
    atm = dfa_minimizer(atm)
    atm.fill_search_capture_map()
    return atm




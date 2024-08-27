from ..classes import *
from ..methods import re_compile
import logging
from typing import List, Dict, Set, Tuple
logger = logging.getLogger(__name__)

def product_dfa(dfa_1: Automat, dfa_2: Automat) -> Automat:
    """
    Product of two DFAs is a DFA that accepts the intersection of the languages of the two DFAs.
    :param dfa_1: First DFA
    :param dfa_2: Second DFA
    :return: Product of two DFAs
    """
    result: Automat = Automat()
    # for state_first in dfa_1.state_map.keys():
    #     for state_second in dfa_2.state_map.keys():
    #         result.add_transition()

    new_alphabet: Set[str] = set()
    for from_dfa_1, values_1 in dfa_1.state_map.items():
        for to_dfa_1, transitions in values_1.items():
            for char, allowed in transitions.items():
                if allowed:
                    new_alphabet.add(char)
    for from_dfa_2, values_2 in dfa_2.state_map.items():
        for to_dfa_2, transitions in values_2.items():
            for char, allowed in transitions.items():
                if allowed:
                    new_alphabet.add(char)

    for char in new_alphabet:
        for from_dfa_1, values_1 in dfa_1.state_map.items():
            for from_dfa_2, values_2 in dfa_2.state_map.items():
                to_dfa_1 = None
                to_dfa_2 = None
                for _to_dfa_1, transitions in values_1.items():
                    if transitions[char]:
                        to_dfa_1 = _to_dfa_1
                for _to_dfa_2, transitions in values_2.items():
                    if transitions[char]:
                        to_dfa_2 = _to_dfa_2
                if to_dfa_1 is None and to_dfa_2 is None:
                    result.add_transition(from_dfa_1 * 100 + from_dfa_2, 1, char)
                elif to_dfa_1 is not None and to_dfa_2 is not None:
                    result.add_transition(from_dfa_1 * 100 + from_dfa_2, to_dfa_1 * 100 + to_dfa_2, char)
                elif to_dfa_1 is not None:
                    result.add_transition(from_dfa_1 * 100 + from_dfa_2, to_dfa_1 * 100 - 1, char)
                elif to_dfa_2 is not None:
                    result.add_transition(from_dfa_1 * 100 + from_dfa_2, (-1) * 100 + to_dfa_2, char)
    result.start = dfa_1.start * 100 + dfa_2.start
    return result
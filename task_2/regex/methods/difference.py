from ..classes import *
from ..methods import re_compile
import logging
from typing import List, Dict, Set
from .product import product_dfa
logger = logging.getLogger(__name__)


def difference_dfa(dfa_1: Automat | str, dfa_2: Automat | str) -> Automat:
    """
    Difference of two automatons which will accept all strings that are accepted by the first automat but not by the second
    :param dfa_1: Automat | str
    :param dfa_2: Automat | str
    :return: Automat
    """
    if type(dfa_1) == str:
        dfa_1 = re_compile(dfa_1)
    if type(dfa_2) == str:
        dfa_2 = re_compile(dfa_2)
    dfa_1.add_state(-1)
    dfa_2.add_state(-1)

    result: Automat = product_dfa(dfa_1, dfa_2)
    for allowed_1 in dfa_1.allowed_set:
        for states_2 in dfa_2.state_map.keys():
            if states_2 not in dfa_2.allowed_set:
                result.allowed_set.add(allowed_1 * 100 - 1)
    result.fill_search_capture_map()
    return result

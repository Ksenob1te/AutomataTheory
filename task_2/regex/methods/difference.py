from ..classes import *
from ..methods import re_compile
import logging
from typing import List, Dict, Set
from .product import product_dfa
logger = logging.getLogger(__name__)

def difference_dfa(dfa_1: Automat, dfa_2: Automat):
    dfa_1.add_state(-1)
    dfa_2.add_state(-1)

    result: Automat = product_dfa(dfa_1, dfa_2)
    for allowed_1 in dfa_1.allowed_set:
        for states_2 in dfa_2.state_map.keys():
            if states_2 not in dfa_2.allowed_set:
                result.allowed_set.add(allowed_1 * 100 + states_2)
    return result
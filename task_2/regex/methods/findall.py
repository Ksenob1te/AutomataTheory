from ..classes import *
from ..methods import re_compile
import logging
from typing import List, Dict, Set
logger = logging.getLogger(__name__)

class Re_Result:
    detection: str = ""
    groups: Dict[int, str] = []

    def __init__(self, detection: str, groups: Dict[int, str]):
        self.detection = detection
        self.groups = groups

    def __str__(self):
        text = f"\nCapture groups: {self.groups}\nResulted detection: {self.detection}\n"
        return text

def re_findall(expr: str | Automat, string: str):
    if type(expr) == str:
        atm: Automat = re_compile(expr)
    else:
        atm: Automat = expr

    atm.current_set.clear()
    atm.current_set.add(atm.start)

    captures: Dict[int, str] = {}
    current_capt_groups: Set[int] = set()
    if atm.capture_groups:
        for capture_group in atm.capture_groups:
            captures[capture_group] = ""

    result: str = ""
    correct: List[Re_Result] = []
    last_result: Re_Result | None = None
    i: int = -1
    last_start = None
    while i < len(string) - 1:
        i += 1
        char = string[i]
        # TODO: fix capture (kinda resolved)
        # for state in atm.current_set:
            # if state in atm.search_capture_map and current_capt_groups != atm.search_capture_map[state]:
            #     if len(current_capt_groups) > len(atm.search_capture_map[state]):
            #         current_capt_groups = atm.search_capture_map[state].copy()
            #         break
            #     else:
            #         new_current: Set[int] = atm.search_capture_map[state].copy()
            #         for capture_group in current_capt_groups:
            #             if capture_group in new_current:
            #                 new_current.remove(capture_group)
            #         current_capt_groups = new_current
            #         break
            # elif state not in atm.search_capture_map:
            #     current_capt_groups.clear()
            #     break
        next_states: Set[int] = next_state_set(atm, atm.current_set, char, False)
        # for capture_group in current_capt_groups:
        #     is_different: bool = False
        for state_1 in atm.current_set:
            for state_2 in next_states:
                if (state_1, state_2) in atm.search_capture_map:
                    for group_id in atm.search_capture_map[(state_1, state_2)]:
                        captures[group_id] += char
                    # is_different = True
                    # break
            # if not is_different:
            #     captures[capture_group] += char
        if len(next_states) == 0:
            atm.current_set.clear()
            atm.current_set.add(atm.start)
            result = ""

            if last_result:
                correct.append(last_result)
                last_start = None
                last_result = None
            for capture_id, res in captures.items():
                captures[capture_id] = ""
            if last_start:
                i = last_start
                last_start = None
            else:
                for to_id, transition in atm.state_map[atm.start].items():
                    if transition[char]:
                        i -= 1
                        break

            # for to_id, transition in atm.state_map[atm.start].items():
            #     if transition[char]:
            #         i -= 1
            #         break
            continue

        atm.current_set = next_states
        if not result:
            last_start = i
        result += char
        for acceptor in atm.allowed_set:
            if acceptor in atm.current_set:
                last_result = Re_Result(result, captures.copy())

            # make it use the longest valid + think on a reset for e.g (abcde)|(bcdf) can crash it

    return correct




from typing import Dict, Set, List, Tuple
from string import digits, ascii_letters, punctuation
from ..my_ast import Operator
from ..status import Status
from copy import copy, deepcopy

alphabet = digits + ascii_letters + punctuation + " "
transition_sieve: Dict[str, bool] = {}


def fill_transition_sieve() -> None:
    if transition_sieve != {}:
        return
    for char in alphabet:
        transition_sieve[char] = False
    transition_sieve[""] = False


class Automat:
    state_map: Dict[int, Dict[int, Dict[str, bool]]] = None
    current_set: Set[int] = None
    allowed_set: Set[int] = None
    capture_groups: Dict[int, Set[Tuple[int, int]]] = None
    search_capture_map: Dict[Tuple[int, int], Set[int]] = None

    start: int = None
    end: int = None
    id: int = None

    def _set_range_automat(self, set_range: Set):
        new_start = self.id + len(set_range)
        new_end = -(self.id + len(set_range))
        new_id = self.id + len(set_range)
        self.allowed_set.clear()
        for i, element in enumerate(set_range):
            self.add_transition(new_start, self.start + i, "")
            self.add_transition(self.start + i, -(self.start + i), element)
            self.add_transition(-(self.start + i), new_end, "")
            self.allowed_set.add(-(self.start + i))
        self.allowed_set.add(new_end)
        self.id = new_id
        self.start = new_start
        self.end = new_end

    def __init__(self, automat_id: int = None, transition: str = None, operator: Operator = None):
        self.state_map = {}
        self.current_set = set()
        self.allowed_set = set()
        self.capture_groups = {}
        if automat_id is None:
            return
        self.start = automat_id
        self.end = -automat_id
        self.id = automat_id
        self.allowed_set.add(-automat_id)
        self.current_set.add(automat_id)
        if transition is not None:
            self.add_transition(automat_id, -automat_id, transition)
            return
        elif operator is not None and operator.type == Operator.Type.SET_RANGE:
            self._set_range_automat(operator.set_range)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __str__(self):
        states_text = ""
        for from_id, value in self.state_map.items():
            for to_id, transition in value.items():
                for condition, status in transition.items():
                    if status:
                        states_text += f"{from_id} ----- {condition} ----> {to_id}\n"
        text = f"""
-Automat------------------------------------------
start: {self.start}, end: {self.end}
allowed_states: {self.allowed_set}
capture_groups: {self.capture_groups}
{states_text}
--------------------------------------------------
"""
        return text

    def _merge(self, atm: 'Automat') -> None:
        if self.id == atm.id:
            return

        def __merge_dicts(a: dict, b: dict, _path=[]):
            for key in b:
                if key in a:
                    if isinstance(a[key], dict) and isinstance(b[key], dict):
                        __merge_dicts(a[key], b[key], _path + [str(key)])
                else:
                    a[key] = b[key]
            return a

        __merge_dicts(self.state_map, atm.state_map)
        for capture_group, state_ids in atm.capture_groups.items():
            self.capture_groups[capture_group] = self.capture_groups.get(capture_group, set())
            for state_id in state_ids:
                self.capture_groups[capture_group].add(state_id)
        # self.start = atm.start
        # self.end = atm.end
    def add_capture(self, transition_ids: Tuple[int, int], capture_id: int) -> None:
        self.capture_groups[capture_id] = self.capture_groups.get(capture_id, set())
        self.capture_groups[capture_id].add(transition_ids)

    def add_capture_all_states(self, capture_id: int) -> None:
        for from_id, value in self.state_map.items():
            # self.add_capture(from_id, capture_id)
            for to_id, transition in value.items():
                self.add_capture((from_id, to_id), capture_id)

    def fill_search_capture_map(self) -> None:
        self.search_capture_map = {}
        if self.capture_groups:
            for capture_id, states in self.capture_groups.items():
                for state in states:
                    self.search_capture_map[state] = self.search_capture_map.get(state, set())
                    self.search_capture_map[state].add(capture_id)

    def add_state(self, from_id: int) -> None:
        self.state_map[from_id] = self.state_map.get(from_id, {})

    def add_transition(self, from_id: int, to_id: int, condition: str) -> None:
        self.state_map[from_id] = self.state_map.get(from_id, {})
        self.state_map[to_id] = self.state_map.get(to_id, {})
        self.state_map[from_id][to_id] = self.state_map[from_id].get(to_id, transition_sieve.copy())
        if len(condition) > 1 or condition not in self.state_map[from_id][to_id]:
            return
        self.state_map[from_id][to_id][condition] = True

    def delete_transition(self, from_id: int, to_id: int, condition: str) -> None:
        if (from_id not in self.state_map) or (to_id not in self.state_map[from_id]) or \
                (condition not in self.state_map[from_id][to_id]):
            return
        self.state_map[from_id][to_id][condition] = False
        if True not in self.state_map[from_id][to_id].values():
            del self.state_map[from_id][to_id]

    def _plus_operator(self) -> None:
        self.add_transition(self.end, self.start, "")

    def _star_operator(self) -> None:
        self.add_transition(self.end, self.start, "")
        self.add_transition(self.start + 1, self.start, "")
        self.add_transition(self.end, self.end + 1, "")
        self.start = self.start + 1
        self.end = self.end + 1
        self.id = self.id + 1
        self.allowed_set.add(self.end)
        self.allowed_set.add(self.start)
        self.add_transition(self.start, self.end, "")

    def _range_automat(self, operator: Operator) -> None:
        starter_atm: Automat = deepcopy(self)
        self.id = self.id + operator.max_repetitions * starter_atm.start
        for i in range(operator.max_repetitions - 1):
            multipleCopy: Automat = Automat()
            for from_id, to_dict in starter_atm.state_map.items():
                for to_id, sieve in to_dict.items():
                    for condition, active in sieve.items():
                        if not active:
                            continue
                        multipleCopy.add_transition(
                            from_id + (
                                ((i + 1) * starter_atm.start) if from_id > 0 else (-(i + 1) * starter_atm.start)),
                            to_id + (((i + 1) * starter_atm.start) if to_id > 0 else (-(i + 1) * starter_atm.start)),
                            condition
                        )
            multipleCopy.start = (i + 2) * starter_atm.start
            multipleCopy.end = starter_atm.end - (i + 1) * starter_atm.start

            for allowed_state in starter_atm.allowed_set:
                multipleCopy.allowed_set.add(allowed_state + (((i + 1) * starter_atm.start) if allowed_state > 0 else (
                            -(i + 1) * starter_atm.start)))
            for current_state in starter_atm.current_set:
                multipleCopy.current_set.add(current_state + (((i + 1) * starter_atm.start) if current_state > 0 else (
                            -(i + 1) * starter_atm.start)))

            temp_end: int = self.end
            self._merge(multipleCopy)
            self.start = starter_atm.start
            self.end = multipleCopy.end
            self.add_transition(temp_end, multipleCopy.start, "")
            self.current_set = multipleCopy.current_set
            self.allowed_set = multipleCopy.allowed_set
        for i in range(operator.min_repetitions, operator.max_repetitions):
            if i == 0:
                self.add_transition(starter_atm.start,
                                    starter_atm.end - (operator.max_repetitions - 1) * starter_atm.start, "")
            elif i == 1:
                self.add_transition(starter_atm.end,
                                    starter_atm.end - (operator.max_repetitions - 1) * starter_atm.start, "")
            else:
                self.add_transition(starter_atm.end - (i - 1) * starter_atm.start,
                                    starter_atm.end - (operator.max_repetitions - 1) * starter_atm.start, "")

    def repeat_automat(self, operator: Operator) -> Status:
        if operator.type is not Operator.Type.REPEAT:
            return Status.WRONG_OPERATOR
        if operator.max_repetitions is not None:
            self._range_automat(operator)
        elif operator.min_repetitions == 0:
            self._star_operator()
        else:
            self._plus_operator()
        return Status.OK

    def cat_automat(self, atm: 'Automat') -> Status:
        self._merge(atm)
        new_id = self.id + atm.id
        new_start = new_id
        new_end = -new_id
        self.add_transition(new_start, self.start, "")
        self.add_transition(atm.end, new_end, "")
        self.add_transition(self.end, atm.start, "")
        # self.allowed_set.clear()
        self.allowed_set.clear()
        self.allowed_set.add(new_end)
        for atm_allowed in atm.allowed_set:
            self.allowed_set.add(atm_allowed)
        self.id = new_id
        self.start = new_start
        self.end = new_end
        return Status.OK

    def alter_automat(self, atm: 'Automat') -> Status:
        self._merge(atm)
        new_id = self.id + atm.id
        new_start = new_id
        new_end = -new_id
        self.add_transition(new_start, self.start, "")
        self.add_transition(new_start, atm.start, "")
        self.add_transition(self.end, new_end, "")
        self.add_transition(atm.end, new_end, "")
        # self.allowed_set.clear()
        self.allowed_set.add(new_end)
        # self.allowed_set.add(self.end)
        self.allowed_set.add(atm.end)
        self.id = new_id
        self.start = new_start
        self.end = new_end
        return Status.OK

    # def set_range_automat(self, operator: Operator):
    #     set_range = operator.set_range
    #     if set_range is None:
    #         return Status.WRONG_OPERATOR


if __name__ == "__main__":
    fill_transition_sieve()
    aut = Automat(1, "a")
    op = Operator("{2, 3}")
    aut._repeat_automat(op)
    x = 1

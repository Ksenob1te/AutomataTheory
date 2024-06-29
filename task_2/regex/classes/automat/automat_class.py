from typing import Dict, Set, List
from string import digits, ascii_letters, punctuation

alphabet = digits + ascii_letters + punctuation + " "


class Automat:
    state_map: Dict[int, Dict[int, Dict[str, bool]]] = None
    current_set: Set[int] = None
    allowed_set: Set[int] = None
    capture_groups: Dict[int, Set[int]] = None

    start: int = None
    end: int = None
    id: int = None


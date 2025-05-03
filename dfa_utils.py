# === dfa/dfa_utils.py ===
from dataclasses import dataclass, field
from typing import List

@dataclass
class Node:
    name: str
    transitions: List["Transition"] = field(default_factory=list)
    is_final: bool = False

@dataclass
class Transition:
    symbol: str
    _from: Node
    _to: Node

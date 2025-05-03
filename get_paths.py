from typing import List, Dict
from dfa.dfa_utils import Node

paths = [
    {"G0": 1, "G1": 0, "G2": 0},
]

path_sequences = [
    {"G0": [[0]], "G1": [[]], "G2": [[]]},
]

def get_path(dfa: List[Node], start: Node, k: int):
    if k < len(paths):
        return paths[k]

    start_idx = len(paths)
    for i in range(start_idx, k + 1):
        new_path_counts = {node.name: 0 for node in dfa}
        new_path_seq = {node.name: [] for node in dfa}

        for node in dfa:
            for transition in node.transitions:
                new_path_counts[transition._to.name] += paths[i - 1][node.name]
                new_path_seq[transition._to.name].extend(
                    [*path, transition.symbol]
                    for path in path_sequences[i - 1][node.name] if path
                )

        paths.append(new_path_counts)
        path_sequences.append(new_path_seq)

# === dfa/evaluator.py ===
from typing import List
from dfa.dfa_utils import Node
from dfa.levenshtein import LD, LD_norm, path_correctness
from dfa.simplify import simplify_action_sequence
from dfa.get_paths import get_path, path_sequences

def evaluate(seq: List[str], dfa: List[Node]) -> float:
    start = dfa[0]
    final = dfa[-1]
    max_pc = 0
    min_ld = len(seq)
    get_path(dfa, start, len(seq) - 1)

    for path in path_sequences[len(seq) - 1][final.name]:
        pc = path_correctness(path[1:], seq[1:])
        ld = LD(path[1:], seq[1:])
        max_pc = max(max_pc, pc)
        min_ld = min(min_ld, ld)

    if max_pc == 1: return max_pc

    for i in range(len(seq) - min_ld, len(seq)):
        for path in path_sequences[len(seq) - i - 1][final.name]:
            pc = path_correctness(path[1:], seq[1:])
            ld = LD(path[1:], seq[1:])
            max_pc = max(max_pc, pc)
            min_ld = min(min_ld, ld)

    if max_pc == 1: return max_pc

    get_path(dfa, start, len(seq) + min_ld)
    for i in range(len(seq), len(seq) + min_ld):
        for path in path_sequences[len(seq) - i - 1][final.name]:
            pc = path_correctness(path[1:], seq[1:])
            ld = LD(path[1:], seq[1:])
            max_pc = max(max_pc, pc)
            min_ld = min(min_ld, ld)

    return max_pc

def evaluate_v2(seq: List[str], dfa: List[Node], optimal_seq: List[str]) -> float:
    simplified_seq, fail_states = simplify_action_sequence(seq, dfa)
    return 1 - LD_norm(simplified_seq[1:], optimal_seq[1:], fail_states)

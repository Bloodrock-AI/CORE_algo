from typing import List, Tuple
from dfa.dfa_utils import Node

def actions_to_states(seq: List[str], dfa: List[Node]) -> List[str]:
    current = dfa[0]
    states_visited = [current.name]
    for idx, action in enumerate(seq):
        if idx == 0: continue
        for transition in current.transitions:
            if transition.symbol == action:
                current = transition._to
                states_visited.append(current.name)
                break
        else:
            break
    return states_visited

def simplify_action_sequence(seq: List[str], dfa: List[Node]) -> Tuple[List[str], int]:
    if not seq:
        return [], 0
    current = dfa[0]
    simplified_seq = [0]
    fail_states = 0
    for idx, action in enumerate(seq):
        if idx == 0: continue
        next_state = None
        for transition in current.transitions:
            if transition.symbol == action:
                next_state = transition._to
                break
        if not next_state:
            fail_states += 1
            simplified_seq.append(action)
            continue
        if next_state.name != current.name:
            simplified_seq.append(action)
        current = next_state
    return simplified_seq, fail_states

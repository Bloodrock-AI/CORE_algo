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


G0 = Node("G0")
G1 = Node("G1")
G2 = Node("G2", is_final=True)

G0.transitions = [
    Transition(symbol="B01'", _from=G0, _to=G0),
    Transition(symbol="A", _from=G0, _to=G1),
]

G1.transitions = [
    Transition(symbol="A", _from=G1, _to=G1),
    Transition(symbol="B01'", _from=G1, _to=G1),
    Transition(symbol="B01", _from=G1, _to=G2),
]

G2.transitions = [
    Transition(symbol="A", _from=G2, _to=G2),
    Transition(symbol="B01'", _from=G2, _to=G2),
]

paths = [
    {
        "G0": 1,
        "G1": 0,
        "G2": 0,
    }
]
path_sequences = [
    {
        "G0": [ [0] ],
        "G1": [ [] ],
        "G2": [ [] ],
    }
]

def get_path(dfa: List[Node], start: Node, k: int):
    if k < len(paths):
        return paths[k]

    start = len(paths)

    for i in range(start, k+1):
        new_path_counts = { node.name: 0 for node in dfa }
        new_path_seq = { node.name: [] for node in dfa }

        for node in dfa:
            for transition in node.transitions:
                new_path_counts[transition._to.name] += paths[i-1][node.name]
               
                new_path_seq[transition._to.name].extend(
                    [*path, transition.symbol] for path in path_sequences[i-1][node.name] if path
                )

        paths.append(new_path_counts)
        path_sequences.append(new_path_seq)

def LD(a: List[str], b: List[str]) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[0] == b[0]:
        return LD(a[1:], b[1:])
    return 1 + min(
        LD(a, b[1:]),
        LD(a[1:], b),
        LD(a[1:], b[1:]),
    )

def LD_norm(a: List[str], b: List[str]) -> float:
    ld = LD(a, b)
    return (2 * ld) / (len(a) + len(b) + ld)

def path_correctness(a: List[str], b: List[str]) -> float:
    return 1 - LD_norm(a, b)

def evaluate(seq: List[str], dfa: List[Node]) -> float:
    
    start = dfa[0]
    final = dfa[-1]
    max_pc = 0
    min_ld = 0

    # case 1: |seq| == |target|
    get_path(dfa, start, len(seq)-1)

    for path in path_sequences[len(seq)-1][final.name]:
        print(f"evaluating: {path} with {seq}")
        pc = path_correctness(path, seq)
        ld = LD(path, seq)
        print(f"pc: {pc}")
        if pc > max_pc:
            max_pc = pc
        print(f"ld: {ld}")
        if ld < min_ld:
            min_ld = ld

    if max_pc == 1: return max_pc

    for i in range(len(seq)-min_ld, len(seq)):
        for path in path_sequences[len(seq)-i-1][final.name]:
            print(f"evaluating: {path} with {seq}")
            pc = path_correctness(path, seq)
            ld = LD(path, seq)
            print(f"pc: {pc}")
            if pc > max_pc:
                max_pc = pc
            print(f"ld: {ld}")
            if ld < min_ld:
                min_ld = ld

    if max_pc == 1: return max_pc

    get_path(dfa, start, len(seq)+min_ld)
    for i in range(len(seq), len(seq)+min_ld):
        for path in path_sequences[len(seq)-i-1][final.name]:
            print(f"evaluating: {path} with {seq}")
            pc = path_correctness(path, seq)
            ld = LD(path, seq)
            print(f"pc: {pc}")
            if pc > max_pc:
                max_pc = pc
            print(f"ld: {ld}")
            if ld < min_ld:
                min_ld = ld

    return max_pc

def actions_to_states(seq: List[str], dfa: List[Node]) -> List[str]:
    """
    Simulates the DFA traversal based on a sequence of actions (starting with 0) 
    and returns the sequence of visited states.

    Args:
        seq (List[str]): The sequence of actions performed by the agent. 
                         The first element should be '0', indicating the initial state.
        dfa (List[Node]): The list of nodes representing the DFA.

    Returns:
        List[str]: The ordered list of state names visited starting from the initial state.

    Notes:
        - Assumes the first element '0' just signals the start; no action is taken for it.
        - If an action does not match any available transition, stops the simulation.
    """
    current = dfa[0]  # Start at initial state
    states_visited = [current.name]

    for idx, action in enumerate(seq):
        if idx == 0:
            # Skip the '0' symbol, it's just a marker for starting point
            continue

        transition_found = False
        for transition in current.transitions:
            if transition.symbol == action:
                current = transition._to
                states_visited.append(current.name)
                transition_found = True
                break

        if not transition_found:
            # Action doesn't match any transition from current node, stop traversal
            break

    return states_visited

def simplify_action_sequence(seq: List[str], dfa: List[Node]) -> List[str]:
    if not seq:
        print("[Simplify] Empty sequence provided.")
        return []

    current = dfa[0]  # Start at initial state
    simplified_seq = [0]  # Always keep the initial '0'

    print(f"[Simplify] Starting at state: {current.name}")
    for idx, action in enumerate(seq):
        if idx == 0:
            # Skip '0' marker
            continue

        next_state = None
        for transition in current.transitions:
            if transition.symbol == action:
                next_state = transition._to
                break

        if next_state is None:
            print(f"[Simplify] Action '{action}' is invalid from state '{current.name}'. Stopping.")
            break

        print(f"[Simplify] Action '{action}' transitions from '{current.name}' to '{next_state.name}'.")

        if next_state.name == current.name:
            print(f"[Simplify] -> State did not change (self-loop). Removing action '{action}' from sequence.")
        else:
            print(f"[Simplify] -> State changed! Keeping action '{action}'.")
            simplified_seq.append(action)

        current = next_state

    print(f"[Simplify] Final simplified sequence: {simplified_seq}")
    return simplified_seq


def main() -> None:
    get_path([G0, G1, G2], G0, 5)
    print(paths[2])
    print(path_sequences[2])
    print(evaluate([0, "A", "B01'"], [G0, G1, G2]))

if __name__ == "__main__":
    main()

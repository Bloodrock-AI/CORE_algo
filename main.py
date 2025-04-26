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

def main() -> None:
    get_path([G0, G1, G2], G0, 5)
    print(paths[2])
    print(path_sequences[2])
    print(evaluate([0, "A", "B01'"], [G0, G1, G2]))

if __name__ == "__main__":
    main()

import networkx as nx
from .config import CYCLE_MIN_LEN, CYCLE_MAX_LEN

def detect_cycles(G):
    cycles = []
    for cycle in nx.simple_cycles(G):
        if CYCLE_MIN_LEN <= len(cycle) <= CYCLE_MAX_LEN:
            cycles.append(sorted(cycle))
    return cycles
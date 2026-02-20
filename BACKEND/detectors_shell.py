import networkx as nx
from .config import SHELL_MIN_HOPS, SHELL_MAX_TX_PER_INTERMEDIATE

def detect_shell_networks(G):
    shells = []

    for source in G.nodes:
        for target in G.nodes:
            if source == target:
                continue

            try:
                for path in nx.all_simple_paths(G, source, target, cutoff=5):
                    if len(path) - 1 >= SHELL_MIN_HOPS:
                        intermediates = path[1:-1]
                        if all(G.degree(n) <= SHELL_MAX_TX_PER_INTERMEDIATE
                               for n in intermediates):
                            shells.append(sorted(path))
            except:
                continue

    return shells
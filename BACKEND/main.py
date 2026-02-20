import time
import pandas as pd

from .validator import validate_csv
from .preprocessing import preprocess
from .graph_builder import build_transaction_graph
from .detectors_cycles import detect_cycles
from .detectors_smurfing import detect_smurfing
from .detectors_shell import detect_shell_networks
from .detectors_velocity import detect_velocity_bursts
from .suspicion_score import compute_scores
from .json_formatter import format_json

def run_engine(csv_file):
    start = time.time()

    df = pd.read_csv(csv_file)
    validate_csv(df)
    df = preprocess(df)

    G = build_transaction_graph(df)

    cycles = detect_cycles(G)
    fan_in, fan_out = detect_smurfing(df)
    shells = detect_shell_networks(G)
    velocity = detect_velocity_bursts(df)

    scores, explain = compute_scores(
        cycles, fan_in, fan_out, shells, velocity

        
    )

    rings = []

    for c in cycles:
        rings.append({"members": c, "type": "cycle", "risk": 95.0})

    for r in fan_in:
        rings.append({"members": r, "type": "smurfing_fanin", "risk": 85.0})

    for r in fan_out:
        rings.append({"members": r, "type": "smurfing_fanout", "risk": 85.0})

    for s in shells:
        rings.append({"members": s, "type": "layered_shell", "risk": 90.0})

    return format_json(scores, explain, rings, start, len(G.nodes))
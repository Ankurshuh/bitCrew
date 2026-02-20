def compute_scores(cycles, fan_in, fan_out, shells, velocity):
    scores = {}
    explanations = {}

    def add(acc, value, label):
        scores[acc] = scores.get(acc, 0) + value
        explanations.setdefault(acc, {})[label] = value

    for c in cycles:
        for acc in c:
            add(acc, 40, f"cycle_length_{len(c)}")

    for group in fan_in:
        for acc in group:
            add(acc, 25, "fan_in")

    for group in fan_out:
        for acc in group:
            add(acc, 25, "fan_out")

    for path in shells:
        for acc in path:
            add(acc, 30, "layered_shell")

    for acc in velocity:
        add(acc, 20, "high_velocity")

    if not scores:
        return {}, {}

    max_score = max(scores.values())

    for acc in scores:
        scores[acc] = round((scores[acc] / max_score) * 100, 2)

    return scores, explanations
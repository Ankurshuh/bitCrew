from .config import VELOCITY_Z_THRESHOLD

def detect_velocity_bursts(df):
    bursts = set()
    counts = df.groupby("sender_id").size()

    if len(counts) == 0:
        return bursts

    mean = counts.mean()
    std = counts.std()

    if std == 0:
        return bursts

    z_scores = (counts - mean) / std

    for acc, z in z_scores.items():
        if z > VELOCITY_Z_THRESHOLD:
            bursts.add(acc)

    return bursts
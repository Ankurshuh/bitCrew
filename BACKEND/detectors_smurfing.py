import numpy as np
from datetime import timedelta
from .config import BASE_SMURF_THRESHOLD, SMURF_TIME_WINDOW_HOURS

def adaptive_threshold(series):
    if len(series) == 0:
        return BASE_SMURF_THRESHOLD
    return max(BASE_SMURF_THRESHOLD, int(np.percentile(series, 95)))

def detect_smurfing(df):
    fan_in = []
    fan_out = []
    window = timedelta(hours=SMURF_TIME_WINDOW_HOURS)

    recv_counts = df.receiver_id.value_counts()
    send_counts = df.sender_id.value_counts()

    fin_th = adaptive_threshold(recv_counts)
    fout_th = adaptive_threshold(send_counts)

    for r, grp in df.groupby("receiver_id"):
        if len(grp) >= fin_th:
            if grp.timestamp.max() - grp.timestamp.min() <= window:
                fan_in.append(sorted(set(grp.sender_id) | {r}))

    for s, grp in df.groupby("sender_id"):
        if len(grp) >= fout_th:
            if grp.timestamp.max() - grp.timestamp.min() <= window:
                fan_out.append(sorted(set(grp.receiver_id) | {s}))

    return fan_in, fan_out
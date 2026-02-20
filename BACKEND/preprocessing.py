import pandas as pd

def preprocess(df):
    df = df.drop_duplicates()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="raise"
    )

    df["sender_id"] = df["sender_id"].astype(str).str.strip()
    df["receiver_id"] = df["receiver_id"].astype(str).str.strip()
    df["amount"] = df["amount"].astype(float)

    return df.sort_values("timestamp")
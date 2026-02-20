REQUIRED_COLUMNS = {
    "transaction_id",
    "sender_id",
    "receiver_id",
    "amount",
    "timestamp"
}

def validate_csv(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
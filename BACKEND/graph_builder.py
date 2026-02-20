import networkx as nx

def build_transaction_graph(df):
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row.sender_id,
            row.receiver_id,
            amount=row.amount,
            timestamp=row.timestamp,
            tx_id=row.transaction_id
        )

    return G
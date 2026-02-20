import time
from collections import defaultdict

def format_json(scores, explain, rings, start, total_nodes):
    suspicious = []
    fraud_rings = []
    acc_rings = defaultdict(list)

    for idx, r in enumerate(rings, 1):
        rid = f"RING_{idx:03d}"

        fraud_rings.append({
            "ring_id": rid,
            "member_accounts": r["members"],
            "pattern_type": r["type"],
            "risk_score": r["risk"]
        })

        for acc in r["members"]:
            acc_rings[acc].append(rid)

    for acc, score in scores.items():
        suspicious.append({
            "account_id": acc,
            "suspicion_score": score,
            "detected_patterns": sorted(list(explain.get(acc, {}).keys())),
            "ring_id": ",".join(sorted(acc_rings[acc]))
        })

    suspicious.sort(key=lambda x: x["suspicion_score"], reverse=True)

    return {
        "suspicious_accounts": suspicious,
        "fraud_rings": fraud_rings,
        "summary": {
            "total_accounts_analyzed": total_nodes,
            "suspicious_accounts_flagged": len(suspicious),
            "fraud_rings_detected": len(fraud_rings),
            "processing_time_seconds": round(time.time() - start, 2)
        }
    }
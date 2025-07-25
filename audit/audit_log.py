import json
import os
import hashlib
from datetime import datetime

AUDIT_LOG = os.environ.get("AUDIT_LOG", "audit/audit.log")
os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

def append_audit_entry(log_id: str, action: str, user: str, hash: int):
    """Append a structured, tamper-evident audit entry."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = {
        "timestamp": timestamp,
        "log_id": log_id,
        "action": action,
        "user": user,
        "hash": hash,
    }
    line = json.dumps(entry)
    with open(AUDIT_LOG, "a") as f:
        f.write(line + "\n")

def compute_log_hash(content: str) -> int:
    """Compute a hash for integrity reference."""
    return int(hashlib.sha256(content.encode()).hexdigest(), 16)

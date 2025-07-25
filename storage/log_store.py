import os
import uuid

LOG_DIRECTORY = os.environ.get("LOG_DIRECTORY", "storage/logs")
os.makedirs(LOG_DIRECTORY, exist_ok=True)

def store_encrypted_log(encrypted_log: str, source: str) -> str:
    """Stores encrypted log in a file and returns the log ID."""
    log_id = str(uuid.uuid4())
    filename = f"{LOG_DIRECTORY}/{log_id}.log"
    with open(filename, "w") as f:
        f.write(encrypted_log)
    return log_id

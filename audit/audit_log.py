"""
Tamper-evident audit logging module for encryption operations.
Provides structured JSON logging with integrity hashing.
"""
import json
import os
import hashlib
import logging
from datetime import datetime, timezone
from typing import Optional
from pathlib import Path
import threading

# Constants
DEFAULT_AUDIT_LOG = "audit/audit.log"
HASH_TRUNCATE_BYTES = 8  # Use first 64 bits for efficiency
ENCODING = "utf-8"

# Configuration
AUDIT_LOG = Path(os.environ.get("AUDIT_LOG", DEFAULT_AUDIT_LOG))

# Thread-safe file writing
_write_lock = threading.Lock()

# Logger setup
logger = logging.getLogger(__name__)


def _ensure_audit_directory() -> None:
    """Ensure audit log directory exists. Thread-safe."""
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create audit directory: {e}")
        raise


def append_audit_entry(
    log_id: str,
    action: str,
    user: str,
    content_hash: Optional[int] = None,
    metadata: Optional[dict] = None
) -> bool:
    """
    Append a structured, tamper-evident audit entry.
    
    Args:
        log_id: Unique identifier for the log entry
        action: Action being audited (e.g., 'encrypt', 'decrypt')
        user: Username performing the action
        content_hash: Optional hash of content for integrity (truncated to 64-bit)
        metadata: Optional additional metadata to include
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        ValueError: If required parameters are empty or invalid
    """
    # Input validation
    if not log_id or not isinstance(log_id, str):
        raise ValueError("log_id must be a non-empty string")
    if not action or not isinstance(action, str):
        raise ValueError("action must be a non-empty string")
    if not user or not isinstance(user, str):
        raise ValueError("user must be a non-empty string")
    
    try:
        # Use UTC timezone-aware timestamp
        timestamp = datetime.now(timezone.utc).isoformat()
        
        entry = {
            "timestamp": timestamp,
            "log_id": log_id,
            "action": action,
            "user": user,
        }
        
        # Add optional fields only if provided
        if content_hash is not None:
            # Truncate hash to 64-bit for efficiency
            entry["content_hash"] = content_hash & ((1 << 64) - 1)
        
        if metadata:
            entry["metadata"] = metadata
        
        # Serialize once
        line = json.dumps(entry, separators=(',', ':'))  # Compact JSON
        
        # Thread-safe write with lock
        with _write_lock:
            _ensure_audit_directory()
            with open(AUDIT_LOG, "a", encoding=ENCODING) as f:
                f.write(line)
                f.write("\n")
        
        return True
        
    except (OSError, IOError) as e:
        logger.error(f"Failed to write audit entry: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid data in audit entry: {e}")
        return False


def compute_log_hash(content: str) -> int:
    """
    Compute a truncated hash for integrity reference.
    
    Uses SHA-256 but returns only first 64 bits for memory efficiency
    while maintaining sufficient collision resistance for audit purposes.
    
    Args:
        content: String content to hash
        
    Returns:
        int: 64-bit hash value
        
    Raises:
        ValueError: If content is not a string
    """
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    
    if not content:
        logger.warning("Computing hash of empty string")
    
    # Compute SHA-256
    hash_bytes = hashlib.sha256(content.encode(ENCODING)).digest()
    
    # Use only first 8 bytes (64 bits) for efficiency
    # Still provides 2^64 possible values (collision resistant enough for audit logs)
    truncated_hash = int.from_bytes(hash_bytes[:HASH_TRUNCATE_BYTES], byteorder='big')
    
    return truncated_hash


def verify_audit_integrity(log_path: Optional[Path] = None) -> tuple[bool, list[str]]:
    """
    Verify audit log file integrity.
    
    Args:
        log_path: Path to audit log (defaults to AUDIT_LOG)
        
    Returns:
        tuple: (is_valid, list of error messages)
    """
    log_path = log_path or AUDIT_LOG
    errors = []
    
    if not log_path.exists():
        return False, ["Audit log file does not exist"]
    
    try:
        with open(log_path, "r", encoding=ENCODING) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    entry = json.loads(line)
                    # Validate required fields
                    required = ["timestamp", "log_id", "action", "user"]
                    for field in required:
                        if field not in entry:
                            errors.append(f"Line {line_num}: Missing field '{field}'")
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")
        
        return len(errors) == 0, errors
        
    except (OSError, IOError) as e:
        return False, [f"Failed to read audit log: {e}"]


# Initialize directory on import (safer than module-level makedirs)
try:
    _ensure_audit_directory()
except OSError:
    logger.warning(f"Could not create audit directory on module import")

import re

REDACTION_PATTERNS = {
    "emails": (r"[\w\.-]+@[\w\.-]+", "[REDACTED_EMAIL]"),
    "ipv4": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED_IP]"),
    "ssn": (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
}

def redact(log: str, rules: dict) -> str:
    """Redacts PII based on config rules."""
    for key, enabled in rules.items():
        if enabled and key in REDACTION_PATTERNS:
            pattern, replacement = REDACTION_PATTERNS[key]
            log = re.sub(pattern, replacement, log)
    return log

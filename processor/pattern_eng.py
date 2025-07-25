#May  require 're' or 'sklearn' if we upgrade to ML tooling
# processor/pattern_engine.py

def detect_patterns(log: str, patterns: list) -> list:
    """Return list of matched patterns."""
    matches = []
    for pattern in patterns:
        if pattern.lower() in log.lower():
            matches.append(pattern)
    return matches

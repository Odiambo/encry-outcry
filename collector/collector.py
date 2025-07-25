# collector/input_collector.py

import json
from processor.pattern_eng import detect_patterns
from processor.redactor import redact
from processor.encryptor import encrypt_log
from storage.log_store import store_encrypted_log
from config.config_mngr import load_config
from audit.audit_logger import append_audit_entry

def handle_log_input(raw_log: str, source: str):
    config = load_config()
    
    matches = detect_patterns(raw_log, config["detection_patterns"])
    redacted = redact(raw_log, config["redaction_rules"])
    encrypted = encrypt_log(redacted, config["encryption"]["key"])

    log_id = store_encrypted_log(encrypted, source)

    append_audit_entry(log_id, action=\"store_log\", user=source, hash=hash(encrypted))
    return log_id

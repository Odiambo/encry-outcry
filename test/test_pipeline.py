import unittest
from processor.redactor import redact
from processor.pattern_engine import detect_patterns

class TestLogPipeline(unittest.TestCase):

    def test_redaction(self):
        rules = {"emails": True, "ipv4": False, "ssn": True}
        log = "User john.doe@example.com has SSN 123-45-6789."
        redacted = redact(log, rules)
        self.assertNotIn("john.doe@example.com", redacted)
        self.assertNotIn("123-45-6789", redacted)

    def test_pattern_detection(self):
        log = "ALERT: SQL injection detected on endpoint"
        patterns = ["SQL injection", "unauthorized"]
        matches = detect_patterns(log, patterns)
        self.assertIn("SQL injection", matches)
        self.assertNotIn("unauthorized", matches)

if __name__ == '__main__':
    unittest.main()

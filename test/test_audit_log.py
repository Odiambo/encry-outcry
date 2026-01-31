"""
Unit tests for audit/audit_log.py module.
Tests memory efficiency, thread safety, error handling, and validation.
"""
import unittest
import json
import os
import threading
import tempfile
from pathlib import Path
from datetime import datetime, timezone

# Set test environment before importing the module
test_dir = tempfile.mkdtemp()
test_log_path = os.path.join(test_dir, "test_audit.log")
os.environ["AUDIT_LOG"] = test_log_path

from audit.audit_log import (
    append_audit_entry,
    compute_log_hash,
    verify_audit_integrity,
    HASH_TRUNCATE_BYTES
)


class TestAuditLog(unittest.TestCase):
    
    def setUp(self):
        """Clean up test log file before each test."""
        if os.path.exists(test_log_path):
            os.remove(test_log_path)
    
    def tearDown(self):
        """Clean up test log file after each test."""
        if os.path.exists(test_log_path):
            os.remove(test_log_path)
    
    def test_append_basic_entry(self):
        """Test basic audit entry creation."""
        result = append_audit_entry(
            log_id="test-123",
            action="encrypt",
            user="alice"
        )
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_log_path))
        
        # Read and verify entry
        with open(test_log_path, "r") as f:
            line = f.readline()
            entry = json.loads(line)
        
        self.assertEqual(entry["log_id"], "test-123")
        self.assertEqual(entry["action"], "encrypt")
        self.assertEqual(entry["user"], "alice")
        self.assertIn("timestamp", entry)
        # Optional fields should not be present
        self.assertNotIn("content_hash", entry)
        self.assertNotIn("metadata", entry)
    
    def test_append_with_content_hash(self):
        """Test audit entry with content hash."""
        large_hash = (1 << 256) - 1  # 256-bit hash
        result = append_audit_entry(
            log_id="test-456",
            action="decrypt",
            user="bob",
            content_hash=large_hash
        )
        
        self.assertTrue(result)
        
        with open(test_log_path, "r") as f:
            entry = json.loads(f.readline())
        
        # Hash should be truncated to 64 bits
        self.assertIn("content_hash", entry)
        truncated = large_hash & ((1 << 64) - 1)
        self.assertEqual(entry["content_hash"], truncated)
    
    def test_append_with_metadata(self):
        """Test audit entry with metadata."""
        metadata = {"file": "secret.txt", "size": 1024}
        result = append_audit_entry(
            log_id="test-789",
            action="encrypt",
            user="charlie",
            metadata=metadata
        )
        
        self.assertTrue(result)
        
        with open(test_log_path, "r") as f:
            entry = json.loads(f.readline())
        
        self.assertEqual(entry["metadata"], metadata)
    
    def test_compact_json_format(self):
        """Test that JSON is compact (no extra whitespace)."""
        append_audit_entry(
            log_id="test-compact",
            action="encrypt",
            user="dave"
        )
        
        with open(test_log_path, "r") as f:
            line = f.readline().strip()
        
        # Compact JSON should not have spaces after colons or commas
        self.assertNotIn(": ", line)
        self.assertNotIn(", ", line)
    
    def test_timezone_aware_timestamp(self):
        """Test that timestamps are timezone-aware (UTC)."""
        append_audit_entry(
            log_id="test-tz",
            action="encrypt",
            user="eve"
        )
        
        with open(test_log_path, "r") as f:
            entry = json.loads(f.readline())
        
        timestamp_str = entry["timestamp"]
        # Parse timestamp and check it's valid ISO format
        timestamp = datetime.fromisoformat(timestamp_str)
        # Should have timezone info
        self.assertIsNotNone(timestamp.tzinfo)
        self.assertEqual(timestamp.tzinfo, timezone.utc)
    
    def test_input_validation_empty_log_id(self):
        """Test validation for empty log_id."""
        with self.assertRaises(ValueError) as cm:
            append_audit_entry(log_id="", action="encrypt", user="alice")
        self.assertIn("log_id", str(cm.exception))
    
    def test_input_validation_empty_action(self):
        """Test validation for empty action."""
        with self.assertRaises(ValueError) as cm:
            append_audit_entry(log_id="123", action="", user="alice")
        self.assertIn("action", str(cm.exception))
    
    def test_input_validation_empty_user(self):
        """Test validation for empty user."""
        with self.assertRaises(ValueError) as cm:
            append_audit_entry(log_id="123", action="encrypt", user="")
        self.assertIn("user", str(cm.exception))
    
    def test_input_validation_non_string_log_id(self):
        """Test validation for non-string log_id."""
        with self.assertRaises(ValueError) as cm:
            append_audit_entry(log_id=123, action="encrypt", user="alice")
        self.assertIn("log_id", str(cm.exception))
    
    def test_thread_safety(self):
        """Test concurrent writes don't corrupt the log."""
        num_threads = 10
        entries_per_thread = 20
        threads = []
        
        def write_entries(thread_id):
            for i in range(entries_per_thread):
                append_audit_entry(
                    log_id=f"thread-{thread_id}-entry-{i}",
                    action="test",
                    user=f"user-{thread_id}"
                )
        
        # Start all threads
        for i in range(num_threads):
            t = threading.Thread(target=write_entries, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
        
        # Verify all entries were written
        with open(test_log_path, "r") as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), num_threads * entries_per_thread)
        
        # Verify all entries are valid JSON
        for line in lines:
            entry = json.loads(line)
            self.assertIn("log_id", entry)
            self.assertIn("action", entry)
            self.assertIn("user", entry)
    
    def test_compute_log_hash_basic(self):
        """Test basic hash computation."""
        content = "test content"
        hash_value = compute_log_hash(content)
        
        # Should be an integer
        self.assertIsInstance(hash_value, int)
        # Should be non-negative
        self.assertGreaterEqual(hash_value, 0)
        # Should fit in 64 bits
        self.assertLess(hash_value, 1 << 64)
    
    def test_compute_log_hash_deterministic(self):
        """Test hash is deterministic."""
        content = "same content"
        hash1 = compute_log_hash(content)
        hash2 = compute_log_hash(content)
        
        self.assertEqual(hash1, hash2)
    
    def test_compute_log_hash_different_content(self):
        """Test different content produces different hashes."""
        hash1 = compute_log_hash("content A")
        hash2 = compute_log_hash("content B")
        
        self.assertNotEqual(hash1, hash2)
    
    def test_compute_log_hash_validation(self):
        """Test hash computation validates input."""
        with self.assertRaises(ValueError):
            compute_log_hash(123)  # Not a string
    
    def test_compute_log_hash_truncation(self):
        """Test hash is properly truncated to 64 bits."""
        import hashlib
        
        content = "test for truncation"
        truncated_hash = compute_log_hash(content)
        
        # Compute full hash manually
        full_hash_bytes = hashlib.sha256(content.encode("utf-8")).digest()
        expected_hash = int.from_bytes(full_hash_bytes[:HASH_TRUNCATE_BYTES], byteorder='big')
        
        self.assertEqual(truncated_hash, expected_hash)
    
    def test_verify_audit_integrity_valid(self):
        """Test integrity verification for valid log."""
        # Write some valid entries
        append_audit_entry("id1", "encrypt", "alice")
        append_audit_entry("id2", "decrypt", "bob", content_hash=12345)
        
        is_valid, errors = verify_audit_integrity(Path(test_log_path))
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_verify_audit_integrity_missing_file(self):
        """Test integrity verification for missing file."""
        missing_path = Path(test_dir) / "nonexistent.log"
        is_valid, errors = verify_audit_integrity(missing_path)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("does not exist", errors[0])
    
    def test_verify_audit_integrity_invalid_json(self):
        """Test integrity verification for invalid JSON."""
        # Write invalid JSON
        with open(test_log_path, "w") as f:
            f.write('{"valid": "entry", "log_id": "1", "action": "test", "user": "alice", "timestamp": "2024-01-01T00:00:00+00:00"}\n')
            f.write('invalid json line\n')
            f.write('{"another": "valid", "log_id": "2", "action": "test", "user": "bob", "timestamp": "2024-01-01T00:00:00+00:00"}\n')
        
        is_valid, errors = verify_audit_integrity(Path(test_log_path))
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("Invalid JSON", errors[0])
    
    def test_verify_audit_integrity_missing_fields(self):
        """Test integrity verification for entries with missing required fields."""
        # Write entry missing required field
        with open(test_log_path, "w") as f:
            # Missing 'user' field
            f.write('{"timestamp": "2024-01-01T00:00:00+00:00", "log_id": "1", "action": "test"}\n')
        
        is_valid, errors = verify_audit_integrity(Path(test_log_path))
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("Missing field", errors[0])
        self.assertIn("user", errors[0])
    
    def test_verify_audit_integrity_empty_lines(self):
        """Test integrity verification ignores empty lines."""
        # Write entries with empty lines
        with open(test_log_path, "w") as f:
            f.write('{"timestamp": "2024-01-01T00:00:00+00:00", "log_id": "1", "action": "test", "user": "alice"}\n')
            f.write('\n')
            f.write('  \n')
            f.write('{"timestamp": "2024-01-01T00:00:00+00:00", "log_id": "2", "action": "test", "user": "bob"}\n')
        
        is_valid, errors = verify_audit_integrity(Path(test_log_path))
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility considerations."""
    
    def test_hash_parameter_renamed(self):
        """Verify that old 'hash' parameter is renamed to 'content_hash'."""
        # This test documents the breaking change
        # Old code: append_audit_entry(log_id="x", action="y", user="z", hash=123)
        # New code: append_audit_entry(log_id="x", action="y", user="z", content_hash=123)
        
        # Verify the new parameter works
        result = append_audit_entry(
            log_id="test",
            action="test",
            user="test",
            content_hash=12345
        )
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

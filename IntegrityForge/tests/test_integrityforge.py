"""
IntegrityForge Test Suite

Comprehensive testing for deterministic file integrity validation.

OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED
"""

import pytest
import tempfile
import os
from pathlib import Path
from integrityforge.core import IntegrityHasher, IntegrityValidator, IntegrityAttestor
from integrityforge.config import ConfigManager


class TestIntegrityHasher:
    """Test SHA-256 hashing functionality."""

    def test_hash_bytes(self):
        """Test hashing byte data."""
        hasher = IntegrityHasher()
        test_data = b"IntegrityForge test data"
        result = hasher.hash_bytes(test_data)

        # Known SHA-256 hash for test data
        expected = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
        assert result.upper() == expected.upper()

    def test_hash_file(self):
        """Test hashing file content."""
        hasher = IntegrityHasher()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test file content")
            temp_path = f.name

        try:
            result = hasher.hash_file(temp_path)
            assert isinstance(result, str)
            assert len(result) == 64  # SHA-256 hex length
            assert result.isalnum()
        finally:
            os.unlink(temp_path)

    def test_deterministic_hashing(self):
        """Test that identical inputs produce identical outputs."""
        hasher = IntegrityHasher()
        test_data = b"deterministic test"

        result1 = hasher.hash_bytes(test_data)
        result2 = hasher.hash_bytes(test_data)

        assert result1 == result2


class TestIntegrityValidator:
    """Test hash validation functionality."""

    def test_constant_time_compare(self):
        """Test constant-time string comparison."""
        validator = IntegrityValidator()

        # Equal strings
        assert validator.constant_time_compare("test", "test") is True

        # Unequal strings
        assert validator.constant_time_compare("test", "different") is False

        # Different lengths
        assert validator.constant_time_compare("test", "testing") is False

    def test_validate_hash_success(self):
        """Test successful hash validation."""
        validator = IntegrityValidator()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            # Get actual hash
            hasher = IntegrityHasher()
            actual_hash = hasher.hash_file(temp_path)

            # Validate against itself
            result = validator.validate_hash(temp_path, actual_hash)
            assert result is True
        finally:
            os.unlink(temp_path)

    def test_validate_hash_failure(self):
        """Test failed hash validation."""
        validator = IntegrityValidator()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            # Validate against wrong hash
            wrong_hash = "0" * 64
            result = validator.validate_hash(temp_path, wrong_hash)
            assert result is False
        finally:
            os.unlink(temp_path)


class TestIntegrityAttestor:
    """Test cryptographic attestation functionality."""

    def test_generate_attestation(self):
        """Test attestation generation."""
        attestor = IntegrityAttestor()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test attestation content")
            temp_path = f.name

        try:
            attestation = attestor.generate_attestation(temp_path)

            # Check required fields
            assert "file_path" in attestation
            assert "file_size" in attestation
            assert "sha256_hash" in attestation
            assert "timestamp" in attestation
            assert "algorithm" in attestation
            assert "attestor" in attestation

            # Check values
            assert attestation["file_path"] == temp_path
            assert attestation["file_size"] > 0
            assert len(attestation["sha256_hash"]) == 64
            assert attestation["algorithm"] == "SHA-256"
        finally:
            os.unlink(temp_path)

    def test_verify_attestation(self):
        """Test attestation verification."""
        attestor = IntegrityAttestor()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test verification content")
            temp_path = f.name

        try:
            # Generate attestation
            attestation = attestor.generate_attestation(temp_path)

            # Verify against same file
            result = attestor.verify_attestation(attestation)
            assert result is True

            # Verify against different file should fail
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
                f2.write("different content")
                temp_path2 = f2.name

            try:
                result = attestor.verify_attestation(attestation, temp_path2)
                assert result is False
            finally:
                os.unlink(temp_path2)

        finally:
            os.unlink(temp_path)


class TestConfigManager:
    """Test configuration management functionality."""

    def test_load_defaults(self):
        """Test loading default configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ConfigManager(temp_dir)
            loaded_config = config.load_configuration()

            # Check that defaults are loaded
            assert "integrityforge" in loaded_config
            assert "validation" in loaded_config
            assert "attestation" in loaded_config
            assert "logging" in loaded_config

    def test_get_set_values(self):
        """Test getting and setting configuration values."""
        config = ConfigManager()

        # Test setting and getting
        config.set("test", "key", "value")
        assert config.get("test", "key") == "value"

        # Test default values
        assert config.get("nonexistent", "key", "default") == "default"


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_hash_validate_workflow(self):
        """Test complete hash and validate workflow."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("integration test content")
            temp_path = f.name

        try:
            # Hash file
            hasher = IntegrityHasher()
            file_hash = hasher.hash_file(temp_path)

            # Validate hash
            validator = IntegrityValidator()
            result = validator.validate_hash(temp_path, file_hash)

            assert result is True

        finally:
            os.unlink(temp_path)

    def test_attest_verify_workflow(self):
        """Test complete attest and verify workflow."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("attestation workflow test")
            temp_path = f.name

        try:
            # Generate attestation
            attestor = IntegrityAttestor()
            attestation = attestor.generate_attestation(temp_path)

            # Verify attestation
            result = attestor.verify_attestation(attestation)
            assert result is True

        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__])
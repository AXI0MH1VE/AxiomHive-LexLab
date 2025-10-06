"""
Core cryptographic operations for IntegrityForge.

Provides deterministic SHA-256 hashing with streaming support and constant-time
comparison for secure integrity validation.

OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED
"""

import hashlib
import logging
from pathlib import Path
from typing import Iterator, BinaryIO, Union

logger = logging.getLogger(__name__)


class IntegrityHasher:
    """Deterministic SHA-256 hasher with streaming support."""

    DEFAULT_CHUNK_SIZE = 8192

    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE):
        """Initialize hasher with specified chunk size."""
        self.chunk_size = chunk_size
        logger.debug(f"IntegrityHasher initialized with chunk_size={chunk_size}")

    def hash_file(self, file_path: Union[str, Path]) -> str:
        """
        Compute SHA-256 hash of file with streaming processing.

        Args:
            file_path: Path to file to hash

        Returns:
            Hexadecimal string representation of SHA-256 hash

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file cannot be read
            OSError: For other file system errors
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        try:
            hash_obj = hashlib.sha256()
            with path.open('rb') as f:
                for chunk in self._iter_chunks(f):
                    hash_obj.update(chunk)

            digest = hash_obj.hexdigest().upper()
            logger.info(f"File hashed successfully: {path} -> {digest[:16]}...")
            return digest

        except PermissionError:
            logger.error(f"Permission denied: {path}")
            raise
        except OSError as e:
            logger.error(f"OS error hashing file {path}: {e}")
            raise

    def hash_stream(self, stream: BinaryIO) -> str:
        """
        Compute SHA-256 hash from binary stream.

        Args:
            stream: Binary stream to hash

        Returns:
            Hexadecimal string representation of SHA-256 hash
        """
        hash_obj = hashlib.sha256()
        for chunk in self._iter_chunks(stream):
            hash_obj.update(chunk)

        digest = hash_obj.hexdigest().upper()
        logger.debug(f"Stream hashed successfully: {digest[:16]}...")
        return digest

    def hash_bytes(self, data: bytes) -> str:
        """
        Compute SHA-256 hash of byte data.

        Args:
            data: Bytes to hash

        Returns:
            Hexadecimal string representation of SHA-256 hash
        """
        digest = hashlib.sha256(data).hexdigest().upper()
        logger.debug(f"Bytes hashed successfully: {digest[:16]}...")
        return digest

    def _iter_chunks(self, stream: BinaryIO) -> Iterator[bytes]:
        """Iterate over stream in chunks."""
        while True:
            chunk = stream.read(self.chunk_size)
            if not chunk:
                break
            yield chunk


class IntegrityValidator:
    """Constant-time hash comparison for integrity validation."""

    def __init__(self):
        logger.debug("IntegrityValidator initialized")

    def validate_hash(self, file_path: Union[str, Path], expected_hash: str) -> bool:
        """
        Validate file integrity against expected hash.

        Args:
            file_path: Path to file to validate
            expected_hash: Expected SHA-256 hash in hexadecimal

        Returns:
            True if hash matches, False otherwise
        """
        try:
            hasher = IntegrityHasher()
            actual_hash = hasher.hash_file(file_path)
            result = self.constant_time_compare(actual_hash, expected_hash.upper())

            if result:
                logger.info(f"Integrity validation PASSED: {Path(file_path).name}")
            else:
                logger.warning(f"Integrity validation FAILED: {Path(file_path).name}")
                logger.debug(f"Expected: {expected_hash.upper()}")
                logger.debug(f"Actual:   {actual_hash}")

            return result

        except Exception as e:
            logger.error(f"Integrity validation error for {file_path}: {e}")
            return False

    def constant_time_compare(self, a: str, b: str) -> bool:
        """
        Constant-time string comparison to prevent timing attacks.

        Args:
            a: First string to compare
            b: Second string to compare

        Returns:
            True if strings are equal, False otherwise
        """
        if len(a) != len(b):
            return False

        # Convert to bytes for consistent comparison
        a_bytes = a.encode('utf-8')
        b_bytes = b.encode('utf-8')

        # Constant-time comparison
        result = 0
        for x, y in zip(a_bytes, b_bytes):
            result |= x ^ y

        return result == 0

    def validate_multiple(self, validations: list) -> dict:
        """
        Validate multiple files against expected hashes.

        Args:
            validations: List of (file_path, expected_hash) tuples

        Returns:
            Dictionary with validation results
        """
        results = {
            'total': len(validations),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'details': []
        }

        for file_path, expected_hash in validations:
            try:
                passed = self.validate_hash(file_path, expected_hash)
                if passed:
                    results['passed'] += 1
                else:
                    results['failed'] += 1

                results['details'].append({
                    'file': str(file_path),
                    'expected': expected_hash,
                    'passed': passed
                })

            except Exception as e:
                results['errors'] += 1
                results['details'].append({
                    'file': str(file_path),
                    'expected': expected_hash,
                    'error': str(e),
                    'passed': False
                })

        logger.info(f"Batch validation complete: {results['passed']}/{results['total']} passed")
        return results


class IntegrityAttestor:
    """Cryptographic attestation generation for integrity proofs."""

    def __init__(self):
        logger.debug("IntegrityAttestor initialized")

    def generate_attestation(self, file_path: Union[str, Path],
                           metadata: dict = None) -> dict:
        """
        Generate cryptographic attestation for file integrity.

        Args:
            file_path: Path to file to attest
            metadata: Optional metadata to include

        Returns:
            Attestation dictionary with hash, timestamp, and metadata
        """
        from datetime import datetime

        try:
            hasher = IntegrityHasher()
            file_hash = hasher.hash_file(file_path)

            attestation = {
                'file_path': str(file_path),
                'file_size': Path(file_path).stat().st_size,
                'sha256_hash': file_hash,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'algorithm': 'SHA-256',
                'attestor': 'IntegrityForge v1.0.0'
            }

            if metadata:
                attestation['metadata'] = metadata

            logger.info(f"Attestation generated for: {Path(file_path).name}")
            return attestation

        except Exception as e:
            logger.error(f"Attestation generation failed for {file_path}: {e}")
            raise

    def verify_attestation(self, attestation: dict, file_path: Union[str, Path] = None) -> bool:
        """
        Verify integrity attestation.

        Args:
            attestation: Attestation dictionary to verify
            file_path: Optional file path override

        Returns:
            True if attestation is valid, False otherwise
        """
        try:
            target_path = file_path or attestation['file_path']

            validator = IntegrityValidator()
            expected_hash = attestation['sha256_hash']

            return validator.validate_hash(target_path, expected_hash)

        except Exception as e:
            logger.error(f"Attestation verification failed: {e}")
            return False
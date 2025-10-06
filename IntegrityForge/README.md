# IntegrityForge

**Deterministic File Integrity Validation and Cryptographic Attestation System**

IntegrityForge provides professional-grade file integrity validation with cryptographic certainty, external configuration management, and automated attestation generation for enterprise environments requiring provable data integrity.

## Features

- **Deterministic SHA-256 Processing**: Streaming file hashing with bounded memory usage
- **Constant-Time Comparison**: Timing attack-resistant hash validation
- **External Configuration**: YAML, INI, and environment variable support
- **Cryptographic Attestation**: Timestamped integrity proofs with metadata
- **Cross-Platform**: Windows, Linux, macOS compatibility
- **Clean Exit Codes**: 0=success, 1=failure, 2=error for CI/CD integration

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/alexisadams/integrityforge.git
cd integrityforge
pip install -r requirements.txt
pip install -e .
```

### Basic Usage

```bash
# Hash a file
integrityforge hash file.txt

# Validate file integrity
integrityforge validate --expected a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 file.txt

# Generate attestation
integrityforge attest file.txt --output attestation.json

# Verify attestation
integrityforge verify attestation.json
```

## Configuration

Create a `config/` directory with validation rules:

```yaml
# config/validation.yml
version: "1.0"
rules:
  - name: "system_binaries"
    pattern: "*.exe,*.dll"
    required: true
    algorithms: ["sha256"]

attestation:
  format: "json"
  include_timestamps: true
```

## CI/CD Integration

### One-Command Validation

```bash
# Validate entire project
./scripts/validate_integrity.sh

# Returns: 0 (success), 1 (failure), 2 (error)
```

### GitHub Actions Example

```yaml
name: Integrity Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install IntegrityForge
      run: pip install -e .
    - name: Validate Artifacts
      run: integrityforge validate --expected ${{ secrets.EXPECTED_HASH }} build/artifact.bin
```

## Command Reference

### Hash Files
```bash
integrityforge hash [OPTIONS] FILES...

Options:
  --chunk-size INTEGER  Chunk size for streaming (default: 8192)
  --output PATH         Output file for hash results
```

### Validate Integrity
```bash
integrityforge validate [OPTIONS] FILE

Options:
  --expected TEXT  Expected SHA-256 hash [required]
  --chunk-size INTEGER  Chunk size for streaming (default: 8192)
```

### Generate Attestation
```bash
integrityforge attest [OPTIONS] FILE

Options:
  --output PATH  Output file for attestation [required]
  --format [json|yaml]  Output format (default: json)
  --metadata TEXT  Additional metadata as JSON string
```

### Verify Attestation
```bash
integrityforge verify [OPTIONS] ATTESTATION

Options:
  --file PATH  File to verify against (overrides path in attestation)
```

### Configuration Management
```bash
integrityforge config [OPTIONS]

Options:
  --validate  Validate current configuration
  --show     Show current configuration
  --save PATH  Save current configuration to file
```

## Exit Codes

- **0**: Success - Operation completed successfully
- **1**: Validation Failure - Integrity check failed
- **2**: Error - Operational error (file not found, permission denied, etc.)
- **3**: Configuration Error - Invalid configuration or arguments

## Security

- SHA-256 cryptographic hashing (NIST-approved)
- Constant-time comparison prevents timing attacks
- Configurable chunk sizes for memory-bounded operation
- No external network dependencies for core operations

## Performance

- **Streaming Processing**: O(1) memory usage regardless of file size
- **Default Chunk Size**: 8192 bytes for optimal I/O performance
- **Configurable Parallelism**: Multi-file batch processing support

## Requirements

- Python 3.8+
- PyYAML (optional, for YAML configuration)
- jsonschema (optional, for configuration validation)

## Architecture

```
integrityforge/
├── core.py          # Cryptographic operations
├── config.py        # Configuration management
├── cli.py           # Command-line interface
└── __init__.py      # Package initialization
```

## Development

### Testing

```bash
# Run test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=integrityforge --cov-report=html
```

### Validation

```bash
# Validate project integrity
./scripts/validate_integrity.sh

# Generate attestation
integrityforge attest STRATEGY.md PRINCIPLES.md DEPLOYMENT.md --output project_attestation.json
```

## License

This project is provided as-is for professional engineering use.

## Support

For enterprise support and custom integrations, contact the maintainer.

---

**OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED**
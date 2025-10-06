# IntegrityForge Deployment Guide

## System Requirements

### Minimum Requirements
- Python 3.8+
- 100 MB available disk space
- 256 MB RAM
- Any modern operating system (Windows, Linux, macOS)

### Recommended Requirements
- Python 3.9+
- 500 MB available disk space
- 512 MB RAM
- SSD storage for optimal performance

## Installation Methods

### Method 1: PyPI Installation (Recommended)

```bash
pip install integrityforge
```

### Method 2: Source Installation

```bash
git clone https://github.com/alexisadams/integrityforge.git
cd integrityforge
pip install -r requirements.txt
pip install -e .
```

### Method 3: Docker Deployment

```bash
docker pull alexisadams/integrityforge:latest
docker run -v $(pwd):/workspace alexisadams/integrityforge validate /workspace/file.txt
```

## Configuration Setup

### 1. Create Configuration Directory

```bash
mkdir -p config/
```

### 2. Runtime Configuration (config/runtime.ini)

```ini
[integrityforge]
chunk_size = 8192
log_level = INFO
progress_reporting = true
max_file_size = 1073741824

[validation]
strict_mode = true
signature_verification = true
timestamp_tolerance = 300

[attestation]
output_format = json
include_metadata = true
compression = gzip
```

### 3. Validation Rules (config/validation.yml)

```yaml
version: "1.0"
rules:
  - name: "system_files"
    pattern: "*.exe,*.dll,*.so,*.dylib"
    required: true
    algorithms: ["sha256"]

  - name: "documents"
    pattern: "*.pdf,*.docx,*.txt"
    required: false
    algorithms: ["sha256"]

  - name: "archives"
    pattern: "*.zip,*.tar.gz,*.7z"
    required: false
    algorithms: ["sha256"]

attestation:
  format: "json"
  include_timestamps: true
  signature_required: true
```

### 4. Environment Variables (.env)

```bash
# IntegrityForge Configuration
INTEGRITYFORGE_CONFIG_DIR=./config
INTEGRITYFORGE_LOG_FILE=./logs/integrityforge.log
INTEGRITYFORGE_CACHE_DIR=./cache

# Security Settings
INTEGRITYFORGE_PRIVATE_KEY=./keys/private.pem
INTEGRITYFORGE_PUBLIC_KEY=./keys/public.pem

# Performance Tuning
INTEGRITYFORGE_CHUNK_SIZE=8192
INTEGRITYFORGE_MAX_WORKERS=4
```

## Basic Usage

### File Hashing

```bash
# Hash a single file
integrityforge hash file.txt

# Hash with specific algorithm
integrityforge hash --algorithm sha256 file.txt

# Hash from stdin
echo "test data" | integrityforge hash -

# Hash multiple files
integrityforge hash file1.txt file2.txt file3.txt
```

### Integrity Validation

```bash
# Validate against known hash
integrityforge validate --expected a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 file.txt

# Validate using manifest file
integrityforge validate --manifest checksums.sha256

# Batch validation
integrityforge validate --batch files.txt
```

### Attestation Generation

```bash
# Generate attestation for file
integrityforge attest file.txt --output attestation.json

# Generate attestation with signature
integrityforge attest file.txt --sign --output attestation.sig

# Batch attestation
integrityforge attest --manifest files.txt --output batch_attestation.json
```

## Advanced Configuration

### Custom Validation Rules

Create `config/custom_rules.yml`:

```yaml
version: "1.0"
custom_rules:
  - name: "critical_system_files"
    pattern: "**/bin/*,**/lib/*"
    severity: "critical"
    actions:
      - "quarantine"
      - "alert"

  - name: "user_data"
    pattern: "**/user/*/data/*"
    severity: "high"
    actions:
      - "backup"
      - "validate"
```

### Integration with CI/CD

#### GitHub Actions Example

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
      run: pip install integrityforge
    - name: Validate Artifacts
      run: integrityforge validate --manifest artifacts.sha256 --strict
    - name: Generate Attestation
      run: integrityforge attest --manifest artifacts.sha256 --output attestation.json
```

#### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    stages {
        stage('Validate') {
            steps {
                sh 'pip install integrityforge'
                sh 'integrityforge validate --manifest build-artifacts.sha256 --strict'
            }
        }
        stage('Attest') {
            steps {
                sh 'integrityforge attest --manifest build-artifacts.sha256 --output attestation.json'
                archiveArtifacts artifacts: 'attestation.json', fingerprint: true
            }
        }
    }
}
```

## Operational Procedures

### Daily Operations

1. **Configuration Backup**: Backup `config/` directory weekly
2. **Log Rotation**: Rotate logs when they exceed 100MB
3. **Key Management**: Rotate cryptographic keys annually
4. **Performance Monitoring**: Monitor processing times and resource usage

### Maintenance Tasks

#### Log Management
```bash
# Rotate logs
integrityforge --rotate-logs

# Archive old logs
find logs/ -name "*.log" -mtime +30 -exec gzip {} \;
```

#### Cache Management
```bash
# Clear hash cache
integrityforge --clear-cache

# Optimize cache
integrityforge --optimize-cache
```

#### Key Rotation
```bash
# Generate new key pair
integrityforge --generate-keys

# Update configuration
integrityforge --update-keys ./keys/new_private.pem
```

### Troubleshooting

#### Common Issues

**Issue**: "Permission denied" errors
**Solution**:
```bash
# Check file permissions
ls -la file.txt

# Run with appropriate permissions
sudo integrityforge validate file.txt
```

**Issue**: "Configuration not found" errors
**Solution**:
```bash
# Check configuration directory
ls -la config/

# Validate configuration
integrityforge --validate-config
```

**Issue**: Slow performance on large files
**Solution**:
```ini
# Increase chunk size in runtime.ini
chunk_size = 65536
max_workers = 8
```

#### Performance Tuning

```ini
# High-performance configuration
[integrityforge]
chunk_size = 131072
max_workers = 8
buffer_size = 1048576

[validation]
parallel_processing = true
memory_limit = 1073741824
```

## Security Considerations

### Key Management
- Store private keys in HSM or secure key vault
- Rotate keys annually or after security incidents
- Backup keys using encrypted storage

### Access Control
- Limit CLI access to authorized users
- Use sudo/su for elevated operations
- Implement audit logging for all operations

### Network Security
- Run in air-gapped environments when possible
- Use TLS for remote attestation
- Implement rate limiting for API endpoints

## Validation Scripts

### One-Command Validation

```bash
# Validate entire project integrity
./scripts/validate_project.sh

# Output: 0 (success) or 1 (failure)
```

### CI/CD Integration Script

```bash
#!/bin/bash
# scripts/ci_validate.sh

set -e

echo "Running IntegrityForge validation..."

# Install if not present
pip install integrityforge

# Validate build artifacts
integrityforge validate --manifest build-artifacts.sha256 --strict

# Generate attestation
integrityforge attest --manifest build-artifacts.sha256 --output attestation.json

# Verify attestation
integrityforge verify attestation.json

echo "Validation complete"
```

## Monitoring and Alerting

### Log Analysis
```bash
# Analyze recent logs
integrityforge --analyze-logs --since "1 hour ago"

# Generate log report
integrityforge --log-report --output security_report.json
```

### Performance Metrics
```bash
# Generate performance report
integrityforge --performance-report --output perf_metrics.json

# Alert on anomalies
integrityforge --check-anomalies --threshold 0.1
```

## Backup and Recovery

### Configuration Backup
```bash
# Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/

# Restore configuration
tar -xzf config_backup_20250115.tar.gz
```

### Key Backup
```bash
# Encrypted key backup
openssl enc -aes-256-cbc -salt -in keys/private.pem -out keys/private.pem.enc

# Key recovery
openssl enc -d -aes-256-cbc -in keys/private.pem.enc -out keys/private.pem
```

## Compliance and Audit

### Audit Trail Generation
```bash
# Generate audit report
integrityforge --audit-report --start-date 2025-01-01 --end-date 2025-01-31 --output audit_202501.pdf
```

### Compliance Validation
```bash
# SOX compliance check
integrityforge --compliance-check sox --output sox_report.json

# GDPR compliance check
integrityforge --compliance-check gdpr --output gdpr_report.json
```

**OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED**
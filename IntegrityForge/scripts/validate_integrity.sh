#!/bin/bash
# IntegrityForge Validation Script
# One-command validation for CI/CD systems
# Exit codes: 0=success, 1=failure, 2=error

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$PROJECT_ROOT/config"
LOG_FILE="/tmp/integrityforge_validation_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}ERROR:${NC} $*" >&2 | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}SUCCESS:${NC} $*" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}WARNING:${NC} $*" | tee -a "$LOG_FILE"
}

# Cleanup function
cleanup() {
    if [[ -f "$LOG_FILE" ]]; then
        log "Log file: $LOG_FILE"
    fi
}

trap cleanup EXIT

# Main validation function
validate_integrity() {
    log "Starting IntegrityForge validation suite"
    log "Project root: $PROJECT_ROOT"
    log "Config directory: $CONFIG_DIR"

    local errors=0
    local warnings=0

    # Check if we're in the right directory
    if [[ ! -f "$PROJECT_ROOT/STRATEGY.md" ]]; then
        error "Not in IntegrityForge project directory"
        return 2
    fi

    # Check Python availability
    if ! command -v python3 &> /dev/null; then
        error "Python 3 not found"
        return 2
    fi

    # Check if integrityforge is available
    if ! python3 -c "import sys; sys.path.insert(0, '$PROJECT_ROOT/src'); import integrityforge" 2>/dev/null; then
        error "IntegrityForge module not found or not importable"
        return 2
    fi

    success "Python environment validated"

    # Validate configuration
    log "Validating configuration..."
    if [[ -d "$CONFIG_DIR" ]]; then
        if python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/src')
from integrityforge.config import ConfigManager
config = ConfigManager('$CONFIG_DIR')
try:
    config.load_configuration()
    print('Configuration loaded successfully')
except Exception as e:
    print(f'Configuration error: {e}', file=sys.stderr)
    sys.exit(1)
        "; then
            success "Configuration validation passed"
        else
            error "Configuration validation failed"
            ((errors++))
        fi
    else
        warning "Configuration directory not found: $CONFIG_DIR"
        ((warnings++))
    fi

    # Validate core functionality
    log "Testing core cryptographic functions..."
    if python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/src')
from integrityforge.core import IntegrityHasher, IntegrityValidator

# Test hashing
hasher = IntegrityHasher()
test_data = b'IntegrityForge test data'
hash_result = hasher.hash_bytes(test_data)
expected = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'

if hash_result.upper() == expected.upper():
    print('Hash function validated')
else:
    print(f'Hash mismatch: got {hash_result}, expected {expected}', file=sys.stderr)
    sys.exit(1)

# Test validation
validator = IntegrityValidator()
if validator.constant_time_compare(hash_result, expected):
    print('Constant-time comparison validated')
else:
    print('Constant-time comparison failed', file=sys.stderr)
    sys.exit(1)
    "; then
        success "Core cryptographic functions validated"
    else
        error "Core cryptographic function validation failed"
        ((errors++))
    fi

    # Test CLI interface
    log "Testing CLI interface..."
    if python3 "$PROJECT_ROOT/src/integrityforge/cli.py" --help >/dev/null 2>&1; then
        success "CLI interface validated"
    else
        error "CLI interface validation failed"
        ((errors++))
    fi

    # Validate project structure
    log "Validating project structure..."
    local required_files=(
        "STRATEGY.md"
        "PRINCIPLES.md"
        "DEPLOYMENT.md"
        "requirements.txt"
        "src/integrityforge/__init__.py"
        "src/integrityforge/core.py"
        "src/integrityforge/config.py"
        "src/integrityforge/cli.py"
    )

    local missing_files=0
    for file in "${required_files[@]}"; do
        if [[ ! -f "$PROJECT_ROOT/$file" ]]; then
            error "Missing required file: $file"
            ((missing_files++))
        fi
    done

    if [[ $missing_files -eq 0 ]]; then
        success "Project structure validated"
    else
        error "Project structure validation failed: $missing_files files missing"
        ((errors++))
    fi

    # Generate integrity attestation
    log "Generating integrity attestation..."
    local attestation_file="$PROJECT_ROOT/validation_attestation_$(date +%Y%m%d_%H%M%S).json"

    if python3 -c "
import sys
import json
from pathlib import Path
sys.path.insert(0, '$PROJECT_ROOT/src')
from integrityforge.core import IntegrityAttestor

attestor = IntegrityAttestor()
results = {}

# Attest core files
core_files = [
    'STRATEGY.md',
    'PRINCIPLES.md',
    'DEPLOYMENT.md',
    'requirements.txt',
    'src/integrityforge/__init__.py',
    'src/integrityforge/core.py',
    'src/integrityforge/config.py',
    'src/integrityforge/cli.py'
]

for file in core_files:
    file_path = Path('$PROJECT_ROOT') / file
    if file_path.exists():
        try:
            attestation = attestor.generate_attestation(file_path)
            results[file] = attestation
        except Exception as e:
            results[file] = {'error': str(e)}

# Write attestation
with open('$attestation_file', 'w') as f:
    json.dump(results, f, indent=2, sort_keys=True)

print(f'Attestation generated: $attestation_file')
    "; then
        success "Integrity attestation generated: $attestation_file"
    else
        error "Integrity attestation generation failed"
        ((errors++))
    fi

    # Summary
    log "Validation complete"
    log "Errors: $errors"
    log "Warnings: $warnings"

    if [[ $errors -gt 0 ]]; then
        error "Validation FAILED with $errors errors"
        return 1
    else
        success "Validation PASSED"
        if [[ $warnings -gt 0 ]]; then
            warning "$warnings warnings detected"
        fi
        return 0
    fi
}

# Run validation
validate_integrity
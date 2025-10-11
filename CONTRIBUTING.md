# Contributing to AxiomHive-LexLab

Thank you for your interest in contributing to AxiomHive-LexLab! We welcome contributions to this precision-grade, auditable NLP and text analytics platform. 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Project Vision](#project-vision)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Security & Compliance](#security--compliance)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Project Vision

AxiomHive-LexLab is built on the principle that **every pipeline is evidence**. Our mission is to provide a verifiable, regulator-ready NLP and text forensics stack that prioritizes:

- ✅ **Traceability** - Every transformation logged and reproducible
- 🔒 **Security** - Cryptographic integrity and audit trails
- 🏔️ **Privacy** - Offline-first, air-gapped deployment capable
- 🔍 **Transparency** - Clear, inspectable logic and deterministic behavior
- 📊 **Compliance** - Built for regulated industries

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Understanding of NLP concepts (helpful but not required for documentation contributions)
- Familiarity with cryptographic concepts (for security-related contributions)

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AxiomHive-LexLab.git
   cd AxiomHive-LexLab
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/AXI0MH1VE/AxiomHive-LexLab.git
   ```
4. **Set up your environment** (details TBD based on setup scripts)
5. **Run initial tests** to verify your setup

## How to Contribute

### Reporting Bugs

- Use the GitHub Issues tab
- Search existing issues first to avoid duplicates
- Include detailed information:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Python version, etc.)
  - Pipeline configuration and audit logs if applicable
  - Hash mismatches or integrity failures if relevant

### Suggesting Features

- Open a GitHub Issue with the "enhancement" label
- Clearly describe:
  - The feature and its use case
  - How it aligns with our security/compliance goals
  - Impact on audit trails and reproducibility
- Discuss in GitHub Discussions for broader community input

### Good First Issues

Look for issues labeled `good first issue` - these are great starting points for new contributors!

## Development Process

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b security/vulnerability-fix
```

### Making Changes

1. Make your changes in your feature branch
2. Follow our [Coding Standards](#coding-standards)
3. Ensure changes maintain audit trail integrity
4. Update or add tests
5. Update documentation
6. Test thoroughly in local/air-gap mode

### Commit Messages

Write clear, descriptive commit messages:

```
type(scope): Brief description (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain the problem this commit solves and why this approach was chosen.

Impact on audit trails, reproducibility, or security should be noted.

Fixes #123
```

**Types**: `feat`, `fix`, `security`, `audit`, `crypto`, `docs`, `test`, `refactor`, `perf`, `chore`

**Scopes**: `pipeline`, `audit`, `crypto`, `api`, `models`, `docs`, `tests`

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use meaningful, descriptive names

### Code Organization

- Keep functions focused and atomic
- Add comprehensive docstrings to all public APIs
- Comment complex cryptographic or NLP logic
- Maintain deterministic behavior - avoid non-reproducible operations

### Example Function:

```python
from typing import Dict, List, Optional
import hashlib

def process_pipeline_stage(
    inputs: List[str],
    config: Dict[str, any],
    audit_log: Optional[Dict] = None
) -> Dict[str, any]:
    """
    Process a single pipeline stage with full audit trail.
    
    Args:
        inputs: Input texts to process
        config: Stage configuration parameters
        audit_log: Optional parent audit log to chain
        
    Returns:
        dict: Result with outputs, hash, and audit record
        
    Raises:
        ValueError: If inputs are invalid
        IntegrityError: If hash verification fails
    """
    # Implementation maintains audit trail
    pass
```

## Security & Compliance

### Critical Principles

1. **Maintain Reproducibility**
   - Same inputs must produce same outputs
   - Document any sources of non-determinism
   - Test across different environments

2. **Preserve Audit Trails**
   - All transformations must be logged
   - Chain audit records via content hashes
   - Never skip audit logging

3. **Cryptographic Integrity**
   - Use approved hash algorithms (SHA-256, BLAKE3, SHA3-256)
   - Follow cryptographic best practices
   - Document security assumptions

4. **Privacy & Air-Gap Compliance**
   - No external API calls by default
   - Vendor all dependencies
   - Support offline operation

### Security Review

- Security-sensitive changes require additional review
- Cryptographic changes need cryptography expert review
- Compliance-impacting changes need documentation updates

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_audit_trail.py

# Run with coverage
pytest --cov=lexlab tests/

# Test reproducibility
pytest tests/test_determinism.py --count=10
```

### Writing Tests

- **Unit tests** for individual functions
- **Integration tests** for pipelines
- **Reproducibility tests** - run same test multiple times, verify identical outputs
- **Audit trail tests** - verify hash chains and logging
- **Security tests** - test integrity verification, error handling

### Test Requirements

- All new features must have tests
- Bug fixes must include regression tests
- Maintain high code coverage (aim for >85%)
- Tests must be deterministic and reproducible

## Documentation

### What to Document

- New features and APIs
- Pipeline stages and transformations
- Configuration options
- Security considerations
- Compliance implications
- Audit trail structure changes

### Documentation Style

- Clear, technical language appropriate for regulated industries
- Include code examples
- Add diagrams for complex workflows
- Document security assumptions and guarantees
- Explain impact on reproducibility and audit trails

### Documentation Structure

```python
"""
Module: Brief description

Longer description explaining purpose, security properties,
and compliance considerations.

Security:
    - Property 1
    - Property 2

Compliance:
    - Consideration 1
    - Consideration 2
"""
```

## Pull Request Process

1. **Update your fork** with upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run full test suite** and ensure all tests pass

3. **Verify reproducibility** - test in clean environment

4. **Update documentation** if needed

5. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues (e.g., "Fixes #123")
   - Describe what changed and why
   - Explain impact on audit trails, security, or compliance
   - Include test results and reproducibility verification

7. **Code Review**:
   - Respond to reviewer feedback
   - Make requested changes in new commits
   - Be patient and respectful
   - Explain technical decisions

8. **Merge**:
   - Once approved, a maintainer will merge your PR
   - Your contribution will be included in the next release! 🎉

## Community

### Getting Help

- **GitHub Discussions**: Ask questions and share ideas
- **GitHub Issues**: Report bugs and request features
- **Pull Requests**: Get code review feedback

### Being a Good Community Member

- Be respectful and welcoming
- Help others when you can
- Share knowledge about NLP, security, and compliance
- Give constructive, technical feedback
- Celebrate successes together! 🎉

### Contribution Areas

- 📝 **Documentation** - Improve clarity, add examples, tutorials
- 🔍 **Testing** - Expand test coverage, reproducibility tests
- ⚡ **Performance** - Optimize pipelines while maintaining audit trails
- 🔒 **Security** - Enhance cryptographic features, vulnerability fixes
- 🧠 **NLP** - Add new analyzers, transformations, models
- 📊 **Compliance** - Improve audit reporting, regulatory documentation
- 🔌 **API** - Extend plugin interfaces, add new capabilities

## Key Principles (Reminder)

When contributing, always keep in mind:

1. **Every pipeline is evidence** - maintain full audit trails
2. **Reproducibility is non-negotiable** - deterministic behavior always
3. **Security through transparency** - clear, inspectable logic
4. **Privacy-first design** - offline/air-gap capable
5. **Built for compliance** - regulatory and legal requirements

## License

By contributing to AxiomHive-LexLab, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask questions in GitHub Discussions or open an issue. We're here to help!

Thank you for contributing to verifiable, reproducible text analytics! 🚀

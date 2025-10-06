# AxiomHive: Sovereign Full-Stack Cognitive Architecture

**A reproducible, transparent, and locally-deployable system for verifiable AI workflows**

AxiomHive is a professional-grade cognitive computing platform built for engineers, researchers, and power users who demand complete control, transparency, and validation over their AI infrastructure. This is not a personality-driven chatbot—it's a rigorous, operator-controlled system designed for sovereignty, security, and reproducible outcomes.

## Why AxiomHive?

In an era of opaque cloud-dependent AI services, AxiomHive provides:

- **Sovereignty & Zero Dependence**: Run entirely offline with airgap-deployable architecture. No external APIs, no telemetry, no vendor lock-in.
- **Transparent Cognitive Logic**: Every reasoning step, safety check, and ethical evaluation is auditable. Open logic means provable outcomes.
- **Operator-Driven Control**: You are not a passive user—you're an operator with direct agency over workflows, validation rules, and system behavior.
- **Security & Integrity by Design**: GPG signing, cryptographic attestation, schema validation, and reproducible builds ensure tamper-proof deployments.
- **Local-First Architecture**: Your data, your compute, your rules. Full-stack deployment runs on your hardware without external dependencies.

## Who Benefits & Why?

**Engineers**: Deploy mission-critical cognitive pipelines with complete auditability and version control.

**Researchers**: Run reproducible experiments with transparent reasoning engines and validation frameworks.

**Security Teams**: Operate AI systems in air-gapped environments with cryptographic proof of integrity.

**Compliance Officers**: Generate provable logic trails for regulatory audits and ethical reviews.

**Power Users**: Take back control from black-box cloud services with a system you can inspect, modify, and validate.

## Empowering Use Cases

- **Sovereign AI Research Assistant**: Deploy a fully local cognitive system for sensitive research without data leaving your infrastructure.
- **Internal Audit & Compliance**: Run automated logical analysis with provable reasoning chains for regulatory documentation.
- **Cognitive Analysis Pipelines**: Build reproducible workflows for pattern detection, reasoning validation, and decision support.
- **Zero-Trust Deployments**: Operate in classified or air-gapped environments with cryptographic integrity attestation.
- **Ethical AI Development**: Transparent safety and ethics modules provide auditable guardrails you control.

## Operator Empowerment

AxiomHive treats you as an **operator**, not a user. This means:

✓ **Direct Agency**: Configure, validate, and modify system behavior at every level.

✓ **Validation Power**: Schema validation, integrity checks, and attestation scripts give you proof, not promises.

✓ **No Hidden Logic**: Every cognitive module is inspectable, debuggable, and under your control.

✓ **Reproducible Outcomes**: Versioned deployments with checksums ensure identical behavior across environments.

This is professional infrastructure for serious applications—not a conversational toy.

---

## Features

- **Backend API**: FastAPI-based backend for handling requests and serving data.
- **Frontend Interface**: React-based frontend built with Vite for a modern web experience.
- **Cognitive Modules**:
  - Emotional Analyzer: Processes and analyzes emotional data.
  - Ethics Sentinel: Ensures ethical compliance in operations.
  - Safety Guardian: Implements OODA loop for safety monitoring.
  - Memory Trace Manager: Manages memory graphs and traces.
  - Reasoning Body: Logical engine for reasoning tasks.
  - Abstract Pattern Detector: Detects patterns in data.
  - Entropy Matrix Harmonizer: Harmonizes entropy matrices for coherence.
  - Monetization Marketplace: Handles marketplace operations.
  - Shard Network: Quantum refractor for network sharding.
- **AxiomHash**: Integrated hashing library for cryptographic operations.
- **CI/CD**: GitHub Actions workflows for continuous integration and validation.
- **Packaging and Attestation**: Scripts for packaging, checksums, and integrity attestation.
- **Validation**: Schema validation for strategy, principles, and deployment.
- **Security**: GPG signing and airgap deployability features.

Quick start (backend):
```
cd backend
python -m pip install -r requirements.txt
./run.sh
```

Quick start (frontend):
```
cd frontend
npm install
npm run dev
```

Run locally (Windows PowerShell)
-------------------------------

From the repository root you can run the backend and serve the frontend with the included helper:

```powershell
.\run_local.ps1
```

The backend will be available at http://127.0.0.1:8000 and the frontend assets (static files) are mounted at http://127.0.0.1:8000/ui/

Packaging and attestation:
```
./scripts/package_zip.sh
./scripts/checksums.sh axiom-v1.0.zip
python scripts/compute_attestation.py
```

Security note: scripts do not perform external network actions by default. Signing requires an explicit `GPG_SIGNER` environment variable.

# Axiomhive Unified Deployment Package

This repository contains the Unified Deployment Package for Alexis Adams' Axiomhive projects. It includes strategy, principles, deployment instructions, and CI validation artifacts for proof-of-integrity and airgap deployability.

See `STRATEGY.md`, `PRINCIPLES.md`, and `DEPLOYMENT.md` for the core manifesto and execution steps.

Local validation (Windows):

Open PowerShell in the repo root and run:

```
.\scripts\compute-integrity.ps1
```

This will compute a SHA256 over the three core markdown files and write `VALIDATION/integrity_attestation.txt`.

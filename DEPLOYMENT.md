## Deployment Guide for Transcendent AI Chatbot

This document provides deployment instructions for local development, containerized environments, and production-grade orchestrations. It complements the repository's validation and attestation workflows.

### Local Development (Windows)

1. Install Python 3.10+ and create a virtual environment:

   python -m venv .venv
   .venv\Scripts\Activate.ps1

2. Install core dev dependencies from `backend/requirements.txt` and `axiomhive/AxiomHash/pyproject.toml` using pip or pipx as appropriate.

3. Run the local validation to verify integrity and tests:

   python .\scripts\validate_workspace.py

### Containerized (Docker)

1. Build the backend image (from `backend/Dockerfile`):

   docker build -t transcendent-backend:latest backend

2. Run with environment variables pointing to attestation and manifest locations.

### Production Orchestration

1. Use a CI/CD pipeline to produce signed ZIP releases. The repository contains GitHub Actions workflows that validate integrity and run tests; adapt these to your environment.

2. Use the `scripts/package_zip.sh` script to create a release bundle and `scripts/checksums.sh` to produce the checksums for release verification.

### Attestation

The repository uses a canonical, kernel-driven SHA-256 attestation recorded in `VALIDATION/integrity_attestation.txt`. To update the attestation after changing the canonical documents, run:

   python supremacy_kernel.py
   # then
   powershell .\scripts\align_attestation.ps1

Ensure the CI pipeline verifies that `legend_manifest.json` computed_sha256 matches `VALIDATION/integrity_attestation.txt`.
Live Execution Vector: Operator Boot Sequence

---

Phase 0: Readiness

```bash
# Visit public launch site
open https://axiomhive.co

# Download the portable deployable
curl -O https://axiomhive.co/downloads/axiom-v1.0.zip
```

---

Phase 1: Local Boot

```bash
unzip axiom-v1.0.zip
cd axiom/
chmod +x install.sh
./install.sh --mode=local
```

* Installs **Runtime Zero**
* Registers **AxiomHive CLI Daemon**
* Initializes **4D Reasoning Loop (temporal/spatial/causal/counterfactual)**

---

Phase 2: Identity Injection

```bash
./axiom id create --handle @devdollzai --keypair ed25519
```

* Generates cryptographically anchored **AxiomSSI** identity

---

Phase 3: Supremacy Stack Execution

```bash
axiom run tesseract
```

* Launches all 5 engines:

	* ⚙️ Forge (Creation)
	* 🧠 Oracle (Perception)
	* 🛠 Agora (Value)
	* ⚔️ Legion (Substrate)
	* 📣 Athena (Narrative)

---

Phase 4: Airgap or Live Deploy

* Compatible with:

	* USB sticks
	* Offline laptops
	* Localhost GitHub Pages
* Optional GitHub Action CI/CD runs integrity validator on commit

---

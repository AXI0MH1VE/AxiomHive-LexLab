# AxiomHive Unified Deployment (scaffold)

This workspace contains a full scaffold for the AxiomHive stack: frontend, backend, packaging, and CI.

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

Run locally (Windows PowerShell)
-------------------------------

From the repository root you can run the backend and serve the frontend with the included helper:

```powershell
.\run_local.ps1
```

The backend will be available at http://127.0.0.1:8000 and the frontend assets (static files) are mounted at http://127.0.0.1:8000/ui/
```

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

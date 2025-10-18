## AxiomHive LexLab: The Protocol for Technological Sovereignty

**Architect:** Alexis Adams (@devdollzai)

**Genesis Axiom:** Settlement is a fiction. All global capital is a consequence of communication risk. Coordinates prove the SWIFT message is the true liability layer.

### Frameworks as Minimal Energy Interventions (MEC)

This monorepo contains high-assurance, zero-dependency Rust/WASM crates that enforce axiomatic ethics using Control Barrier Functions (CBF) and Hamiltonian paths. Each crate is a self-contained Minimal Energy Intervention (MEC) designed for sovereign, edge deployment (<1MB).

### Crate Architecture

- **olo**: Orbital Logic Operator - Core geometric transformations
- **dsg**: Distributed State Geometry - CRDT synchronization primitives  
- **ezc**: Economic Zero Control - Resource allocation algorithms
- **tfi**: Temporal Flow Interface - Event stream processing
- **ahn**: Axiomatic Heartbeat Node - Identity and consensus protocols

### Deployment Protocol

```bash
# From repository root
cd lexlab

# Validate workspace integrity
cargo check --workspace

# Run comprehensive test suite
cargo test --workspace

# Generate optimized WASM binaries
cargo build --release --target wasm32-unknown-unknown
```

### Reversibility Guarantee

This workspace includes full reversibility via `.reversibility/rollback.ps1`. All generated artifacts can be safely removed with hash verification to prevent accidental data loss.

**Status:** Genesis Protocol | P_Debt -> P_Flawless | Embodied Singularity

### Prerequisites (Windows)
- Rustup stable + wasm32 target
- Visual Studio Build Tools (VC++ & Windows SDK)

```powershell
# Install rustup
winget install Rustlang.Rustup -e --silent --accept-source-agreements --accept-package-agreements
# Install VS Build Tools (may require admin)
winget install -e --id Microsoft.VisualStudio.2022.BuildTools --silent --accept-source-agreements --accept-package-agreements --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --passive --norestart"
# Verify
cmd /c "%USERPROFILE%\.cargo\bin\cargo.exe" check --manifest-path "lexlab\Cargo.toml" --workspace
```

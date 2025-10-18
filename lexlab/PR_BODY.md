# PR: Add Rust workspace under lexlab/ with reversibility and UTF-8 LF

## Summary
- Rust workspace bootstrapped under `lexlab/` with five minimal crates: `olo`, `dsg`, `ezc`, `tfi`, `ahn`.
- UTF-8 LF normalization via `.gitattributes` + `.editorconfig`.
- Full reversibility system: `.reversibility/manifest.json` + `rollback.ps1` with hash-verified deletes.
- No root files modified; integrates cleanly with existing repository.

## Technical triad (per request)
- Rust workspace now bootstrapped, `cargo check` and `cargo test` pass, `wasm32-unknown-unknown` enabled.
- Source is modular, audit-ready, quantum-conscious. Anything missed?
- Ready to integrate the OLO crate as phase one protocol.

## Verification (Windows)
- Installed toolchain: rustup stable + wasm32 target; Visual Studio Build Tools (VC++).
- Commands used:
  - `cargo check --manifest-path lexlab/Cargo.toml --workspace`
  - `cargo test  --manifest-path lexlab/Cargo.toml --workspace`

## Next steps
- Phase-1: Integrate OLO crate implementation and example WASM demo.
- Phase-2: CI matrices for lint/test/build (Windows/Linux/macOS) + wasm.
- Phase-3: Docs expansion and security model (CBF, Hamiltonian paths) mapping.

# Phase 3 Batch 3 — Integration and Validation

Phase 3 Batch 3 closes the Phase 3 development cycle and prepares Mifa 1.2.0
for release.

## Scope

This batch intentionally adds no new Method contracts. It integrates and
validates the engine and method work completed in Phase 3 Batch 1 and Batch 2.

## Changes

### Full-catalog release compilation

`tools/release_validate.py` now compiles payload-required presets as part of the
release matrix by supplying deterministic harmless fixtures that satisfy the
declared Payload Contract v2.

This removes the previous payload-required compile skips while preserving:

- temporary build workspaces
- explicit payload type validation
- explicit staging transforms
- source/staged provenance
- no generated binaries committed to the repository

### Expanded smoke bundles

`tools/prepare_smoke.py` now covers 13 curated methods:

- 7 Phase 2 foundation/regression methods
- 6 Phase 3 advanced local inspection methods

The smoke builder supports payload-aware build fixtures and emits:

- Windows executables
- text/Base64/hex runtime fixture data
- `run_smoke.ps1`
- `smoke_manifest.json`

### Release quality

The release-quality test suite now validates:

- version `1.2.0`
- 34 methods
- 60 presets
- Phase 3 release documentation
- Phase 3 smoke coverage

### CI

CI now validates the full compile matrix and prepares both x64 and x86 curated
smoke bundles.

## Release gate

Before tagging `v1.2.0`:

1. Python syntax must pass.
2. All unit tests must pass.
3. All 34 Method contracts must validate.
4. All 60 presets must validate.
5. The environment doctor must pass with all four MinGW-w64 compilers.
6. The payload-aware compile matrix must complete with zero failures.
7. x64 and x86 smoke bundles must build successfully.
8. Both Windows runtime smoke runners must complete with zero failures.
9. The final strict-Git release validation must pass from a clean tree.

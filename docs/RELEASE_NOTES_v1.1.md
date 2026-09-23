# Mifa v1.1.0 Release Notes

Mifa v1.1.0 extends the v1.0 Windows/PE research foundation with a typed
parameter engine, richer compatibility metadata, reusable Windows technique
foundations, and release-quality validation tooling.

## Engine

- typed method parameters: `str`, `int`, `float`, `bool`
- CLI overrides with repeatable `--set KEY=VALUE`
- preset parameter defaults
- parameter precedence: CLI -> preset -> method default
- `choices`, `min`, and `max` validation
- `raw` and `c_string` source rendering
- runtime-argument contracts
- per-method build-type constraints
- resolved parameters recorded in `build.json`
- stronger payload/build compatibility checks

## Technique foundations

Added:

- `win32-api-resolve`
- `win32-local-buffer`
- `win32-local-thread`
- `win32-dll-load-info`
- `win32-file-map`
- `win32-runtime-helper`

These methods remain scoped to local-process primitives, read-only inspection,
module/address research, file mapping, and benign thread lifecycle behavior.

## Quality and release tooling

Added:

- `tools/doctor.py`
- `tools/release_validate.py`
- `tools/prepare_smoke.py`
- release-quality regression tests
- GitHub Actions CI
- automated x64/x86 compile-matrix validation for payload-free presets
- tracked-artifact checks
- curated Windows smoke bundle generation

## Catalog

- 28 method contracts
- 24 Windows research/foundation methods
- 4 regression/test methods
- 48 presets

## Validation

The v1.0 x64 foundation remained the stable baseline.

Phase 2 Batch 1 passed its parameter-engine unit and build validation.

Phase 2 Batch 2 passed:

- 15/15 unit tests at the Batch 2 checkpoint
- 28/28 method contract validation
- x64 compilation for all six Batch 2 methods
- Windows x64 runtime smoke testing for all six Batch 2 methods

The final v1.1 release gate completed successfully. The automated release
matrix compiled 47 payload-free presets with zero failures, with one
payload-required preset intentionally skipped. The curated Windows x86
smoke set completed 7/7 runtime tests with exit code 0.

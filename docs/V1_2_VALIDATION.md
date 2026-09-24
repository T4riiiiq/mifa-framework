# Mifa v1.2.0 Validation

This document records the release gates for Mifa v1.2.0.

## Catalog

Expected release catalog:

```text
Methods : 34
Presets : 60
```

The catalog contains 30 Windows analysis/foundation methods and 4
regression/test methods.

## Phase 3 Batch 1 baseline

Payload Contract v2 added:

- raw/text/json/PE adapters
- copy/Base64/hex staging transforms
- source and staged SHA-256 provenance
- payload-aware manifest fields

Batch 1 validation completed successfully before commit.

## Phase 3 Batch 2 baseline

Six advanced local inspection foundations were added:

```text
win32-payload-inspect
win32-file-buffer
win32-base64-buffer
win32-hex-buffer
win32-pe-runtime-info
win32-pe-section-characteristics
```

Pre-Batch-3 validation completed with:

```text
36 unit tests passed
34/34 method contracts valid
60/60 presets valid
57 payload-free presets compiled
3 payload-required presets skipped by the old release validator
0 failures
```

Windows runtime testing completed successfully for all six new methods on both
x64 and x86.

## Batch 3 automated release gate

Run:

```bash
python3 -m py_compile mifa.py core/*.py tools/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
python3 tools/doctor.py --require-compilers

python3 tools/release_validate.py \
  --compile \
  --json dist/v1.2-release-validation.json
```

Expected compile behavior:

```text
60 presets compiled
3 payload-required presets compiled with deterministic harmless fixtures
0 payload skips
0 failures
```

## Curated runtime gate

Prepare both bundles:

```bash
python3 tools/prepare_smoke.py --arch x64
python3 tools/prepare_smoke.py --arch x86
```

Expected output:

```text
dist/v1.2-smoke-x64/
dist/v1.2-smoke-x86/
```

Each bundle contains 13 binaries plus runtime fixture data and
`run_smoke.ps1`.

On the matching Windows test environment run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_smoke.ps1
```

The expected result is:

```text
Tests: 13
Failures: 0
```

for both architectures.

## Final Git gate

After committing Batch 3, run:

```bash
python3 tools/release_validate.py \
  --compile \
  --strict-git \
  --json dist/v1.2-release-validation.json
```

Only after the strict-Git gate and both Windows smoke runs pass should the
branch be fast-forwarded into `main` and tagged `v1.2.0`.

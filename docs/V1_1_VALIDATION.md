# Mifa v1.1 Validation Plan

Mifa v1.1 is released only after the following gates pass.

## Automated gates

Run from the repository root:

```bash
python3 -m py_compile mifa.py core/*.py tools/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
python3 tools/doctor.py --require-compilers
python3 tools/release_validate.py \
  --compile \
  --json dist/v1.1-release-validation.json
```

The release validator checks:

- every method contract
- every preset reference
- preset parameter resolution
- architecture/build-type compatibility
- tracked generated/binary artifacts
- the full unit-test suite
- a temporary compile matrix for every payload-free preset

Payload-requiring presets are validated but intentionally skipped by the
compile matrix unless a release-safe fixture is supplied by a future workflow.

## Windows runtime gates

The Phase 2 Batch 2 x64 runtime smoke test was completed successfully for:

- `win32-api-resolve`
- `win32-local-buffer`
- `win32-local-thread`
- `win32-dll-load-info`
- `win32-file-map`
- `win32-runtime-helper`

Before tagging v1.1.0, prepare and run the x86 smoke bundle:

```bash
python3 tools/prepare_smoke.py --arch x86
```

The resulting directory is:

```text
dist/v1.1-smoke-x86/
```

The curated x86 smoke set contains the six Phase 2 foundation methods plus
`parameter-test`.

Do not create the `v1.1.0` tag until the x86 smoke set has run successfully on
the Windows lab and the repository is clean.


## Final v1.1.0 result

Final release validation completed successfully:

- 20/20 automated tests passed
- 28/28 method contracts valid
- 48/48 presets valid
- 47 payload-free presets compiled successfully
- 1 payload-required preset intentionally skipped
- 6/6 Phase 2 foundation methods passed Windows x64 runtime smoke testing
- 7/7 curated Windows x86 smoke tests completed with exit code 0
- release validation failures: 0

# Mifa

Mifa is a modular Windows research and build framework written in Python.

It generates, validates, cross-compiles, and tracks reusable C/C++ methods for
Windows internals, PE analysis, process and module inspection, local-memory
research, payload/data handling, and reusable Windows runtime foundations.

**Current development version:** `1.2.0`

---

## Status

Mifa v1.2 release candidate contains:

- 34 valid method contracts
- 30 Windows research/foundation methods
- 4 regression/test methods
- 60 presets
- typed build-time parameters
- runtime-argument contracts
- Payload Contract v2
- payload source/staged provenance with SHA-256 tracking
- `raw`, `text`, `json`, and `pe` payload adapters
- `copy`, `base64`, and `hex` staging transforms
- x64 and x86 MinGW-w64 build support
- payload-aware automated release validation
- curated Windows x64/x86 smoke bundles
- generated PowerShell runtime smoke runner

Phase 3 Batch 1 and Batch 2 validation is complete. The `v1.2.0` tag is created
only after the final Batch 3 release gates and curated x64/x86 smoke bundles
complete successfully.

---

## Architecture

```text
Method Contract
      ↓
Preset
      ↓
Parameter Resolution
      ↓
Compatibility Validation
      ↓
Payload Contract v2 (when required)
      ↓
Payload Adapter / Staging Transform
      ↓
Source Generation
      ↓
MinGW-w64 Compilation
      ↓
Build Manifest + Provenance
      ↓
Windows Output
```

Parameter precedence is:

```text
CLI --set
   ↓
Preset parameters
   ↓
Method defaults
```

Payload handling is intentionally explicit:

```text
Source payload
   ↓
Type validation
   ↓
Selected staging transform
   ↓
Staged artifact
   ↓
Source + staged provenance
```

Every normal Mifa build receives a unique identifier:

```text
K-0001
K-0002
K-0003
...
```

---

## Core Features

- JSON method contracts
- Method and preset discovery
- Schema validation
- Architecture compatibility validation
- Payload Contract v2 validation
- Typed payload adapters
- Explicit payload staging transforms
- Source/staged payload provenance
- Typed method parameters
- Repeatable `--set KEY=VALUE`
- Preset parameter defaults
- `choices`, `min`, and `max` parameter constraints
- Runtime-argument metadata
- Multi-file source generation
- C compilation
- C++17 compilation
- x64 MinGW-w64 support
- x86 MinGW-w64 support
- Static C++ runtime linking
- Debug and release builds
- Unique build IDs
- Build manifests
- Compiler command provenance
- Output SHA-256 hashing
- Environment doctor
- Payload-aware automated release validation
- Curated Windows smoke bundles
- Generated runtime smoke script and fixture data

---

## Method Catalog

### Process and Threads

| Method | Purpose |
|---|---|
| `win32-process-info` | Current process and host information |
| `win32-process-enum` | Enumerate running processes |
| `win32-process-tree` | Display a process descendant tree |
| `win32-thread-enum` | Enumerate threads belonging to a PID |
| `win32-local-thread` | Benign local worker-thread lifecycle |

### Modules and Runtime Images

| Method | Purpose |
|---|---|
| `win32-module-enum` | Enumerate loaded modules |
| `win32-loaded-image` | Translate an RVA using the actual loaded module base |
| `win32-module-layout` | Correlate PE sections with runtime addresses |
| `win32-api-resolve` | Resolve and report a Win32 export address |
| `win32-dll-load-info` | Map a DLL without resolving dependencies and report module information |
| `win32-runtime-helper` | Multi-source C++ helper architecture foundation |

### Virtual Memory, Files, and Local Buffers

| Method | Purpose |
|---|---|
| `win32-memory-map` | Enumerate virtual-memory regions |
| `win32-memory-region` | Inspect one virtual-memory region |
| `win32-self-memory-lab` | Benign local allocation and RW -> R transition |
| `win32-local-buffer` | Parameterized local buffer lifecycle |
| `win32-file-map` | Read-only file mapping with bounded hex preview |
| `win32-file-buffer` | Read a runtime file into a local data buffer |
| `win32-base64-buffer` | Decode Base64 into a local inspection-only buffer |
| `win32-hex-buffer` | Decode hexadecimal data into a local inspection-only buffer |

### Payload and Contract Inspection

| Method | Purpose |
|---|---|
| `win32-payload-inspect` | Report Payload Contract v2 build metadata without loading or executing content |

### PE Analysis

| Method | Purpose |
|---|---|
| `win32-pe-info` | Parse PE headers and sections |
| `win32-pe-rva` | Translate RVA to raw offset and preferred VA |
| `win32-pe-imports` | Parse imported DLLs and symbols |
| `win32-pe-exports` | Parse named exports |
| `win32-pe-datadirs` | Display PE data directories |
| `win32-pe-relocations` | Parse base relocation blocks |
| `win32-pe-section-lookup` | Inspect a named PE section |
| `win32-pe-bytes` | Read bounded file-backed bytes using an RVA |
| `win32-pe-runtime-info` | Inspect PE machine, format, image base, entry point, and subsystem from a runtime-selected file |
| `win32-pe-section-characteristics` | Display file-backed PE section layout and characteristics |

### Regression Methods

| Method | Purpose |
|---|---|
| `hello-world` | C generation and compilation regression |
| `cpp-hello` | C++ generation and compilation regression |
| `payload-test` | Payload Contract v2 staging and provenance regression |
| `parameter-test` | Parameter rendering and runtime-contract regression |

---

## Payload Contract v2

A payload-aware method can declare accepted types, staging transforms, and size
limits.

Supported payload types:

```text
raw
text
json
pe
```

Supported staging transforms:

```text
copy
base64
hex
```

Example:

```bash
python3 mifa.py build \
  --preset payload-test-x64 \
  --payload ./input.txt \
  --payload-type text \
  --payload-transform base64
```

The build manifest records source and staged metadata separately, including
filename, size, and SHA-256.

---

## Requirements

Mifa uses only the Python standard library at runtime.

Build dependencies:

```text
Python 3
MinGW-w64
```

Compiler targets:

```text
x64 C    : x86_64-w64-mingw32-gcc
x64 C++  : x86_64-w64-mingw32-g++

x86 C    : i686-w64-mingw32-gcc
x86 C++  : i686-w64-mingw32-g++
```

Check the local environment:

```bash
python3 tools/doctor.py --require-compilers
```

---

## Usage

List methods:

```bash
python3 mifa.py methods
```

Validate method contracts:

```bash
python3 mifa.py check
```

Inspect a method:

```bash
python3 mifa.py info win32-payload-inspect
```

List presets:

```bash
python3 mifa.py presets
```

Validate a preset:

```bash
python3 mifa.py validate win32-file-buffer-x64
```

Build with preset defaults:

```bash
python3 mifa.py build \
  --preset win32-local-buffer-x64
```

Override declared parameters:

```bash
python3 mifa.py build \
  --preset win32-local-buffer-x64 \
  --set buffer_size=8192 \
  --set fill_byte=90
```

---

## Build Workspace

Example:

```text
builds/K-0035/
├── build.json
├── input/
├── source/
│   └── main.c
└── output/
    └── payload-test.exe
```

The build manifest can record:

```text
Build ID
Method
Architecture
Build type
Resolved parameters
Runtime-argument contract
Payload contract
Payload source provenance
Payload staged provenance
Generated sources
Compiler command
Output filename
Output size
Output SHA-256
```

---

## Release Validation

Run the full automated release gate:

```bash
python3 -m py_compile mifa.py core/*.py tools/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
python3 tools/doctor.py --require-compilers

python3 tools/release_validate.py \
  --compile \
  --json dist/v1.2-release-validation.json
```

The v1.2 release validator compiles every valid preset in a temporary workspace.
Payload-required methods receive deterministic harmless build fixtures so the
compile matrix covers the complete preset catalog without placing generated
artifacts in `builds/`.

Prepare the curated Windows smoke bundles:

```bash
python3 tools/prepare_smoke.py --arch x64
python3 tools/prepare_smoke.py --arch x86
```

Output:

```text
dist/v1.2-smoke-x64/
dist/v1.2-smoke-x86/
```

Each bundle includes:

```text
13 Windows smoke-test executables
smoke-test.txt
smoke-test.b64
smoke-test.hex
run_smoke.ps1
smoke_manifest.json
```

Copy the bundle to Windows and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_smoke.ps1
```

The runner records each program's output and exit code in
`runtime-results.txt` and returns non-zero if a smoke test fails.

---

## Repository Layout

```text
Mifa/
├── mifa.py
├── VERSION
├── README.md
├── core/
├── methods/
├── presets/
├── payloads/
├── builds/
├── dist/
├── docs/
├── tools/
├── tests/
└── .github/
```

---

## Validation History

Mifa v1.0 established the Windows/PE foundation and x64 runtime baseline.

Mifa v1.1 added the typed parameter engine, six Windows technique foundations,
release validation, CI, and completed curated Windows x64/x86 runtime
validation.

Phase 3 Batch 1 added Payload Contract v2, typed adapters, explicit staging
transforms, and source/staged provenance.

Phase 3 Batch 2 added six advanced local inspection foundations. All six passed
the automated compile matrix and completed Windows x64 and x86 runtime smoke
testing.

Phase 3 Batch 3 integrates payload-aware full-catalog release compilation,
expanded smoke tooling, release documentation, and the final v1.2 release
gates.

---

## Documentation

```text
docs/V1_METHOD_MATRIX.md
docs/RELEASE_NOTES_v1.0.md
docs/PHASE2_BATCH1_ENGINE.md
docs/PHASE2_BATCH2_TECHNIQUE_FOUNDATIONS.md
docs/V1_1_VALIDATION.md
docs/RELEASE_NOTES_v1.1.md
docs/PHASE3_BATCH1_RUNTIME_PAYLOAD.md
docs/PHASE3_BATCH2_ADVANCED_METHOD_FOUNDATIONS.md
docs/PHASE3_BATCH3_INTEGRATION_VALIDATION.md
docs/V1_2_VALIDATION.md
docs/RELEASE_NOTES_v1.2.md
```

---

## Version

```text
Mifa 1.2.0 release candidate
```

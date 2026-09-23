# Mifa

Mifa is a modular Windows research and build framework written in Python.

It generates, validates, cross-compiles, and tracks reusable C/C++ methods for
Windows internals, PE analysis, process and module inspection, virtual-memory
research, and reusable local Windows runtime foundations.

**Current version:** `1.1.0`

---

## Status

Mifa v1.1 contains:

- 28 valid method contracts
- 24 Windows research/foundation methods
- 4 regression/test methods
- 48 presets
- typed build-time parameters
- runtime-argument contracts
- x64 and x86 MinGW-w64 build support
- automated release validation
- build provenance and SHA-256 tracking

Windows x64 and x86 runtime smoke validation has been completed for the Phase 2 foundation set.

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
Source Generation
      ↓
MinGW-w64 Compilation
      ↓
Build Manifest
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
- Payload contract validation
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
- Automated release validation
- Curated Windows smoke bundles

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

### Virtual Memory and Mapping

| Method | Purpose |
|---|---|
| `win32-memory-map` | Enumerate virtual-memory regions |
| `win32-memory-region` | Inspect one virtual-memory region |
| `win32-self-memory-lab` | Benign local allocation and RW -> R transition |
| `win32-local-buffer` | Parameterized local buffer lifecycle |
| `win32-file-map` | Read-only file mapping with bounded hex preview |

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

### Regression Methods

| Method | Purpose |
|---|---|
| `hello-world` | C generation and compilation regression |
| `cpp-hello` | C++ generation and compilation regression |
| `payload-test` | Payload contract and staging regression |
| `parameter-test` | Parameter rendering and runtime-contract regression |

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
python3 mifa.py info win32-local-buffer
```

List presets:

```bash
python3 mifa.py presets
```

Validate a preset:

```bash
python3 mifa.py validate win32-local-buffer-x64
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
builds/K-0030/
├── build.json
├── input/
├── source/
│   └── main.cpp
└── output/
    └── win32-local-buffer.exe
```

The build manifest records:

```text
Build ID
Method
Architecture
Build type
Resolved parameters
Runtime-argument contract
Payload metadata
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
  --json dist/v1.1-release-validation.json
```

The release validator compiles every payload-free preset in a temporary
workspace, so the compile matrix does not pollute `builds/`.

Prepare the curated x86 Windows smoke set:

```bash
python3 tools/prepare_smoke.py --arch x86
```

Output:

```text
dist/v1.1-smoke-x86/
```

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

Phase 2 Batch 1 added the typed parameter engine and passed its unit/build
validation.

Phase 2 Batch 2 added six Windows foundation methods. All six compiled for x64
and successfully completed Windows x64 runtime smoke testing.

The final v1.1 release gate adds automated x64/x86 compile-matrix validation
and a curated Windows x86 runtime smoke test before the `v1.1.0` tag is
created.

---

## Documentation

```text
docs/V1_METHOD_MATRIX.md
docs/RELEASE_NOTES_v1.0.md
docs/PHASE2_BATCH1_ENGINE.md
docs/PHASE2_BATCH2_TECHNIQUE_FOUNDATIONS.md
docs/V1_1_VALIDATION.md
docs/RELEASE_NOTES_v1.1.md
```

---

## Version

```text
Mifa 1.1.0
```

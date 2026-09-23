# Mifa

Mifa is a modular Windows research and build framework written in Python.

It generates, validates, cross-compiles, and tracks reusable C/C++ methods for Windows internals, PE analysis, process inspection, module inspection, and virtual-memory research.

**Current version:** `1.0.0`

---

## Status

Mifa v1.0 includes:

- 21 valid method contracts
- 18 Windows research methods
- 3 regression/test methods
- x64 build validation
- x64 Windows runtime validation
- x86 build support
- Build provenance and SHA-256 tracking

> x86 runtime validation is not claimed for v1.0.

---

## Architecture

```text
Method
  ↓
Preset
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

Every build receives a unique identifier:

```text
K-0001
K-0002
K-0003
...
```

Each build workspace records generated source files, compiler information, output metadata, and SHA-256 hashes.

---

## Core Features

- JSON method contracts
- Method and preset discovery
- Schema validation
- Architecture compatibility validation
- Payload contract validation
- Payload staging
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

---

## Method Catalog

### Process

| Method | Purpose |
|---|---|
| `win32-process-info` | Current process and host information |
| `win32-process-enum` | Enumerate running processes |
| `win32-process-tree` | Display a process descendant tree |
| `win32-thread-enum` | Enumerate threads belonging to a PID |

### Modules and Runtime Images

| Method | Purpose |
|---|---|
| `win32-module-enum` | Enumerate loaded modules |
| `win32-loaded-image` | Translate an RVA using the actual loaded module base |
| `win32-module-layout` | Correlate PE sections with runtime addresses |

### Virtual Memory

| Method | Purpose |
|---|---|
| `win32-memory-map` | Enumerate virtual-memory regions |
| `win32-memory-region` | Inspect one virtual-memory region |
| `win32-self-memory-lab` | Benign local memory allocation and RW -> R transition |

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

---

## Requirements

Mifa v1.0 uses only the Python standard library.

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

---

## Usage

List available methods:

```bash
python3 mifa.py methods
```

Validate the method catalog:

```bash
python3 mifa.py check
```

Expected v1.0 result:

```text
21 methods checked
21 valid
0 invalid
```

Inspect a method:

```bash
python3 mifa.py info win32-pe-info
```

List presets:

```bash
python3 mifa.py presets
```

Validate a preset:

```bash
python3 mifa.py validate win32-pe-info-x64
```

Build a method:

```bash
python3 mifa.py build --preset win32-pe-info-x64
```

---

## Build Workspace

Example:

```text
builds/K-0027/
├── build.json
├── input/
├── source/
│   └── main.cpp
└── output/
    └── win32-pe-bytes.exe
```

The build manifest tracks:

```text
Build ID
Method
Architecture
Build type
Build status
Generated sources
Compiler command
Payload metadata
Output filename
Output size
Output SHA-256
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
└── tests/
```

---

## Validation

The Mifa v1.0 x64 catalog was cross-compiled using MinGW-w64 on Kali Linux and runtime-tested on Windows x64.

Validation covered:

- Process inspection
- Process enumeration
- Process trees
- Thread enumeration
- Module enumeration
- Loaded module addressing
- Runtime module layout
- PE header parsing
- RVA translation
- Import parsing
- Export parsing
- Data directories
- Base relocations
- Section lookup
- RVA byte inspection
- Virtual-memory mapping
- Memory-region inspection
- Local memory lifecycle

x86 presets and build support are included, but x86 runtime validation remains a future validation task.

---

## Documentation

See:

```text
docs/V1_METHOD_MATRIX.md
docs/RELEASE_NOTES_v1.0.md
```

---

## Version

```text
Mifa 1.0.0
```

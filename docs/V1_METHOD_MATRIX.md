# Mifa v1.0 Method Matrix

Mifa v1.0 provides a modular Windows build and research framework with
validated x64 Windows/PE foundation methods.

## Validation Status

- Method contracts: 21/21 valid
- Real methods: 18
- Regression/test methods: 3
- x64 build validation: completed
- x64 runtime validation: completed
- x86 build support: available
- x86 runtime validation: not yet completed

---

## Core / Regression Methods

| Method | Purpose |
|---|---|
| `hello-world` | Basic C multi-file regression method |
| `cpp-hello` | Basic C++ multi-file regression method |
| `payload-test` | Payload contract and staging regression method |

---

## Windows Process Methods

| Method | Purpose |
|---|---|
| `win32-process-info` | Collect current process and host information |
| `win32-process-enum` | Enumerate running processes |
| `win32-process-tree` | Display a process descendant tree |
| `win32-thread-enum` | Enumerate threads belonging to a process |

---

## Windows Module / Runtime Methods

| Method | Purpose |
|---|---|
| `win32-module-enum` | Enumerate modules loaded in a process |
| `win32-loaded-image` | Translate RVA using an actual runtime module base |
| `win32-module-layout` | Correlate PE sections with runtime module addresses |

---

## Windows Memory Methods

| Method | Purpose |
|---|---|
| `win32-memory-map` | Enumerate process virtual memory regions |
| `win32-memory-region` | Query metadata for a specific virtual address |
| `win32-self-memory-lab` | Demonstrate benign local RW -> R memory lifecycle |

---

## PE Analysis Methods

| Method | Purpose |
|---|---|
| `win32-pe-info` | Parse PE headers and section metadata |
| `win32-pe-rva` | Translate RVA to raw file offset and preferred VA |
| `win32-pe-imports` | Parse the PE import directory |
| `win32-pe-exports` | Parse named PE exports |
| `win32-pe-datadirs` | Display PE data directories |
| `win32-pe-relocations` | Parse base relocation blocks |
| `win32-pe-section-lookup` | Inspect a named PE section |
| `win32-pe-bytes` | Read bounded file-backed bytes using an RVA |

---

## Mifa v1.0 Core Capabilities

- Method discovery
- JSON method contracts
- Preset discovery
- Contract/schema validation
- Architecture compatibility validation
- Payload staging and SHA-256 metadata
- Multi-file source generation
- Template rendering
- C support
- C++17 support
- x64 cross-compilation
- x86 cross-compilation
- Static MinGW C++ runtime linking
- Release and debug build modes
- Unique build IDs
- Build manifests
- Generated-source tracking
- Compiler command provenance
- Output SHA-256 hashing
- Successful/failed build status tracking

---

## Validation Environment

The v1.0 x64 method catalog was built on Kali Linux using the
MinGW-w64 cross-compilation toolchain and runtime-tested on Windows x64.

The x86 presets and compilation paths are available but are not marked
runtime-validated in v1.0.

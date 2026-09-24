# Mifa

Mifa is a modular Windows security and build framework written in Python.

It provides reusable method contracts, compatibility validation, deterministic
source generation, cross-compilation, payload/data handling, Windows platform
inspection, and structured build provenance.

**Current version:** `2.0.0`

---

## Status

Mifa v2.0 contains:

- 45 valid method contracts
- 82 x64/x86 presets
- 7 first-class technique aliases
- 5 supporting inspection/helper capabilities
- Quick and Inspect CLI workflows
- typed build-time parameters
- runtime-argument contracts
- Payload Contract v2
- source/staged SHA-256 provenance
- x64 and x86 MinGW-w64 compilation
- automated full-preset release validation
- curated Windows runtime smoke bundles

Compilation validation and Windows runtime validation are tracked separately.

---

## CLI

~~~text
[1/q] Quick
[2/i] Inspect
[3/m] Methods
[4/b] Builds
[5/v] Verify
[0/x] Exit
~~~

Examples:

~~~bash
mifa q native -a x64
mifa q reflect -a x64

mifa i inject
mifa i managed
mifa i amsi
mifa i kernel

mifa methods
mifa builds
mifa verify --strict
~~~

Direct Method IDs remain supported:

~~~bash
mifa q win32-pe-runtime-info -a x64
~~~

---

## Technique Layer

| Alias | Method | Scope |
|---|---|---|
| `native` | `win32-local-thread` | Native local thread lifecycle |
| `inject` | `win32-inject-lab` | Target-process compatibility |
| `dll` | `win32-dll-injection-lab` | DLL / target compatibility |
| `reflect` | `win32-reflective-map-lab` | Reflective PE mapping inspection |
| `hollow` | `win32-hollow-lab` | Suspended-process compatibility |
| `managed` | `win32-managed-lab` | CLR / managed PE inspection |
| `jscript` | `win32-jscript-lab` | JScript / script-host inspection |

Supporting capabilities:

| Alias | Method | Role |
|---|---|---|
| `amsi` | `win32-amsi-inspect` | Inspect |
| `appcontrol` | `win32-appcontrol-inspect` | Inspect |
| `trusted` | `win32-trusted-hosts` | Helper |
| `runner` | `win32-runner-helper` | Helper |
| `kernel` | `kernel-security` | Inspect |

The supporting layer does not modify security controls, execute supplied
payloads, load drivers, or modify kernel state.

---

## Architecture

~~~text
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
Payload Adapter / Transform
      ↓
Source Generation
      ↓
MinGW-w64 Compilation
      ↓
Build Manifest + Provenance
      ↓
Windows Output
~~~

Parameter precedence:

~~~text
CLI --set
   ↓
Preset parameters
   ↓
Method defaults
~~~

---

## Payload Contract v2

Supported input types:

~~~text
raw
text
json
pe
~~~

Supported transforms:

~~~text
copy
base64
hex
~~~

Payload-aware builds record source and staged provenance separately, including
size, transform, and SHA-256.

---

## Requirements

Mifa uses only the Python standard library at runtime.

Build requirements:

~~~text
Python 3
MinGW-w64
~~~

Compiler targets:

~~~text
x64 C    : x86_64-w64-mingw32-gcc
x64 C++  : x86_64-w64-mingw32-g++

x86 C    : i686-w64-mingw32-gcc
x86 C++  : i686-w64-mingw32-g++
~~~

Verify the environment:

~~~bash
mifa verify --strict
~~~

---

## Build and Inspect

Inspect a capability:

~~~bash
mifa i hollow
~~~

Quick-build a technique:

~~~bash
mifa q hollow -a x64
~~~

Traditional direct Method and Preset workflows remain available.

Generated workspaces record source files, compiler provenance, output metadata,
and SHA-256 information.

---

## Release Validation

Run the v2 automated release gate:

~~~bash
python3 -m py_compile mifa.py core/*.py tools/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
python3 tools/verify.py --strict

python3 tools/release_validate.py \
  --compile \
  --json dist/v2.0-release-validation.json
~~~

Expected catalog:

~~~text
45 methods
82 presets
82 compiled presets
0 failures
~~~

---

## Windows Smoke Bundles

Prepare both architectures:

~~~bash
python3 tools/prepare_smoke.py --arch x64
python3 tools/prepare_smoke.py --arch x86
~~~

Output:

~~~text
dist/v2.0-smoke-x64/
dist/v2.0-smoke-x86/
~~~

Runtime results are tracked separately from compile validation.

---

## Repository Layout

~~~text
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
~~~

---

## Documentation

Current v2 documentation:

~~~text
docs/TECHNIQUE_COVERAGE_MATRIX.md
docs/PHASE4_BATCH1_CLI_EXPERIENCE.md
docs/PHASE4_BATCH3_RELEASE.md
docs/V2_VALIDATION.md
docs/RELEASE_NOTES_v2.0.md
~~~

Previous release documentation remains available under `docs/`.

---

## Version

~~~text
Mifa 2.0.0
~~~

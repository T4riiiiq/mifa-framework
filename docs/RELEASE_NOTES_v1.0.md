# Mifa v1.0.0

First stable foundation release of Mifa.

## Highlights

Mifa v1.0 establishes the project's modular build system and Windows
research foundation.

The release includes:

- 21 method contracts
- 18 Windows research methods
- 3 regression/test methods
- C and C++17 generation
- x64 and x86 MinGW-w64 build support
- Static C++ runtime linking
- Multi-file method support
- Payload contracts and staging
- Compatibility validation
- Build manifests and provenance
- Output SHA-256 tracking
- Windows process, module, memory, and PE analysis foundations

## Runtime Validation

The complete v1.0 x64 foundation catalog was runtime-tested on Windows x64.

The following areas were validated:

- Process discovery and metadata
- Process trees and thread enumeration
- Module enumeration
- Runtime module base addressing
- PE header parsing
- RVA / raw offset translation
- Import parsing
- Export parsing
- Data directory parsing
- Base relocation parsing
- PE section inspection
- File-backed RVA byte inspection
- Virtual memory mapping
- Individual memory region inspection
- Benign self-process memory allocation/protection lifecycle

## Architecture Status

### x64

Build validated and runtime validated.

### x86

Build infrastructure and presets are included. Runtime validation is
reserved for a later validation pass.

## Scope

Mifa v1.0 focuses on deterministic Windows/PE/memory foundations.

More advanced technique-specific modules belong to later development
milestones rather than the v1.0 foundation release.

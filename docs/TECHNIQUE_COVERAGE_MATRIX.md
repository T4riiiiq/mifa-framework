# Mifa Technique Coverage Matrix

## Purpose

This document tracks the Windows technique families, execution paths, helpers,
and platform capabilities represented in Mifa.

Status values:

- `Implemented` - already available in Mifa.
- `Foundation Exists` - supporting primitives are already available.
- `Candidate Technique` - planned as a first-class Technique Method.
- `Helper` - supports one or more techniques but is not a primary method.
- `Inspect Only` - exposed for inspection, compatibility, or guidance.
- `Deferred` - intentionally outside the current scope.

---

## Script and Managed Execution

| Capability | Mifa Mapping | Status |
|---|---|---|
| JScript execution | `jscript` | Candidate Technique |
| Managed assembly hosting | `managed` | Candidate Technique |
| Win32 API access from managed code | Existing Win32 foundations | Foundation Exists |
| Managed payload runner | `managed` | Candidate Technique |
| Script-host integration | `jscript` | Helper |
| Reflective managed loading concepts | `reflect` | Inspect Only |

---

## Process and Memory

| Capability | Mifa Mapping | Status |
|---|---|---|
| Process injection family | `inject` | Candidate Technique |
| DLL injection family | `dll` | Candidate Technique |
| Reflective PE / DLL loading | `reflect` | Candidate Technique |
| Process hollowing | `hollow` | Candidate Technique |
| Process enumeration | `win32-process-enum` | Implemented |
| Thread enumeration | `win32-thread-enum` | Implemented |
| Module enumeration | `win32-module-enum` | Implemented |
| Memory map inspection | `win32-memory-map` | Implemented |
| Memory region inspection | `win32-memory-region` | Implemented |
| API resolution | `win32-api-resolve` | Implemented |
| PE parsing and address translation | Existing PE methods | Implemented |

---

## Native and Managed Paths

| Capability | Mifa Mapping | Status |
|---|---|---|
| Native Windows execution foundation | `native` | Foundation Exists |
| Native C / C++ Win32 foundations | Existing methods | Implemented |
| Managed execution path | `managed` | Candidate Technique |
| Local thread lifecycle | `win32-local-thread` | Implemented |
| Local buffer lifecycle | `win32-local-buffer` | Implemented |
| Runtime helper support | `win32-runtime-helper` | Implemented |

---

## Payload Handling

| Capability | Mifa Mapping | Status |
|---|---|---|
| Raw payload input | Payload Contract v2 | Implemented |
| PE payload input | Payload Contract v2 | Implemented |
| Text input | Payload Contract v2 | Implemented |
| JSON input | Payload Contract v2 | Implemented |
| Base64 transform | Payload Contract v2 | Implemented |
| Hex transform | Payload Contract v2 | Implemented |
| Payload metadata inspection | `win32-payload-inspect` | Implemented |
| Runtime payload integration | `runner` | Helper |

---

## Security Control Compatibility

| Capability | Mifa Mapping | Status |
|---|---|---|
| File and payload inspection | Existing payload / PE methods | Foundation Exists |
| Payload transformation | Payload Contract v2 | Implemented |
| Managed execution constraints | `managed` | Candidate Technique |
| AMSI compatibility information | `amsi` | Inspect Only |
| Script-host compatibility | `jscript` | Helper |
| Application-control compatibility | `appcontrol` | Inspect Only |
| Trusted execution hosts | `trusted` | Helper |

---

## Application Control

| Capability | Mifa Mapping | Status |
|---|---|---|
| Trusted path behavior | `appcontrol` | Inspect Only |
| DLL policy behavior | `appcontrol` | Inspect Only |
| Alternate data stream behavior | `appcontrol` | Inspect Only |
| Managed runtime restrictions | `appcontrol` | Inspect Only |
| PowerShell language-mode constraints | `appcontrol` | Inspect Only |
| Trusted .NET hosts | `trusted` | Helper |
| Script hosting | `trusted` / `jscript` | Helper |
| Native trusted-host compatibility | `trusted` | Helper |

---

## Kernel Security

| Capability | Mifa Mapping | Status |
|---|---|---|
| Kernel architecture inspection | `kernel` | Inspect Only |
| Callback visibility | `kernel` | Inspect Only |
| Driver requirements | `kernel` | Inspect Only |
| Kernel memory integrity concepts | `kernel` | Inspect Only |
| Object visibility concepts | `kernel` | Inspect Only |
| Windows build compatibility | `kernel` | Inspect Only |

Internal Method ID:

`kernel-security`

---

## Scope Boundaries

The current Mifa scope is focused on Windows execution, payload handling,
process and memory primitives, compatibility, and supporting platform
capabilities.

The following areas remain outside the current scope:

- full command-and-control infrastructure
- network tunneling frameworks
- proxy infrastructure
- Linux execution frameworks
- automated security-product discovery
- automatic technique selection

---

# Planned Technique Set

First-class candidates:

1. `inject`
2. `dll`
3. `reflect`
4. `hollow`
5. `native`
6. `managed`
7. `jscript`

Supporting capabilities:

8. `amsi`
9. `appcontrol`
10. `trusted`
11. `runner`
12. `kernel`

This set should be finalized before implementation begins.

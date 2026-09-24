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
| JScript compatibility inspection | `jscript` | Implemented |
| Managed PE / CLR compatibility inspection | `managed` | Implemented |
| Win32 API access from managed code | Existing Win32 foundations | Foundation Exists |
| Managed image inspection | `managed` | Implemented |
| Script-host compatibility | `jscript` | Implemented |
| Reflective managed loading concepts | `reflect` | Inspect Only |

---

## Process and Memory

| Capability | Mifa Mapping | Status |
|---|---|---|
| Process injection compatibility | `inject` | Implemented |
| DLL injection compatibility | `dll` | Implemented |
| Reflective PE / DLL mapping compatibility | `reflect` | Implemented |
| Process hollowing compatibility | `hollow` | Implemented |
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
| Native Windows execution foundation | `native` | Implemented |
| Native C / C++ Win32 foundations | Existing methods | Implemented |
| Managed PE compatibility path | `managed` | Implemented |
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
| Managed execution constraints | `managed` | Implemented |
| AMSI compatibility information | `amsi` | Inspect Only |
| Script-host compatibility | `jscript` | Implemented |
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

First-class techniques:

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

The first-class technique layer is implemented at the current compatibility and inspection scope.

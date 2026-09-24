# Mifa v2.0 Release Notes

## Overview

Mifa v2.0 introduces the Technique Layer, supporting platform capabilities,
and the Quick and Inspect CLI workflows while preserving the deterministic
Method and Preset build model.

## Release Inventory

- 45 Method contracts
- 82 x64/x86 Presets
- 7 first-class Technique aliases
- 5 supporting capability aliases
- Payload Contract v2
- full-preset automated compilation
- Windows x64/x86 smoke tooling

## First-Class Techniques

`native`, `inject`, `dll`, `reflect`, `hollow`, `managed`, and `jscript`.

The current implementations focus on controlled local behavior,
compatibility, and inspection.

## Supporting Capabilities

`amsi`, `appcontrol`, `trusted`, `runner`, and `kernel`.

These capabilities are inspection/helper paths and do not modify
security-control configuration or kernel state.

## Validation States

- `build-tested` means source generation and supported x64/x86 compilation passed.
- `runtime-tested` means the generated Windows output also completed its intended runtime check.

Compilation and Windows runtime validation are tracked separately.

## Release Validation

The v2 release gate covers Method contracts, Presets, unit tests, compiler
availability, tracked-artifact hygiene, and the complete Preset compile matrix.

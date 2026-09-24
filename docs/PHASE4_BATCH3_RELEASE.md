# Phase 4 Batch 3 - v2 Release Integration

## Scope

Batch 3 finalizes the v2 release after completion of the CLI and Technique
layers.

It covers:

- version transition to 2.0.0
- release documentation
- release-quality gates
- expanded smoke tooling
- full-catalog compile validation
- repository hygiene validation

## Catalog

~~~text
45 methods
82 presets
~~~

## First-Class Layer

~~~text
native
inject
dll
reflect
hollow
managed
jscript
~~~

## Supporting Layer

~~~text
amsi
appcontrol
trusted
runner
kernel
~~~

## Validation Principle

Compilation status and Windows runtime status are independent.

A Method is promoted from `build-tested` to `runtime-tested` only after its
runtime behavior is validated on Windows.

## Final Gate

~~~bash
python3 tools/release_validate.py \
  --compile \
  --json dist/v2.0-release-validation.json
~~~

The v2.0.0 tag is created only after final validation completes successfully.

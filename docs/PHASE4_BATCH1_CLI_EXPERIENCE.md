# Phase 4 Batch 1 — CLI and Interactive Experience

Phase 4 Batch 1 establishes the human-facing workflow that the Technique Layer
will use later in Phase 4.

## Goals

- preserve the existing v1.2 engine and contracts
- add the neutral `Quick` workflow for fast selection
- add the detailed `Inspect` workflow
- rename the old `Doctor` environment check to `Verify`
- add a compact Mifa furnace-inspired terminal banner
- add dependency-free terminal colors
- keep redirected output plain
- add a first-class `mifa` launcher
- preserve existing commands

## Primary workflows

```bash
mifa
mifa quick
mifa q
mifa q peinfo
mifa q filebuf --arch x86
mifa inspect
mifa i
mifa i win32-pe-runtime-info
mifa i peinfo
mifa verify
mifa verify --strict
```

## Existing commands

The existing commands remain available:

```text
methods
check
info
presets
validate
build
```

## Color behavior

Colors are enabled only when standard output is a terminal and `NO_COLOR` is
not set. They can also be disabled explicitly:

```bash
mifa --no-color methods
```

## Launcher

Install the convenience command with:

```bash
python3 tools/install_cli.py
```

This creates:

```text
~/.local/bin/mifa
```

as a symbolic link to the repository launcher.

## Technique Layer compatibility

The Quick alias registry is intentionally separate from the build engine.
Phase 4 Batch 2 can add technique aliases without redesigning the CLI or build
contracts.

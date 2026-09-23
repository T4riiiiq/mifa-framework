# Phase 2 — Batch 1: Engine Upgrade

Batch 1 extends the Mifa v1.0 engine without changing the behavior of existing
method contracts.

## Added

- Declarative method parameters
- Preset parameter defaults/overrides
- Repeatable CLI `--set KEY=VALUE`
- Parameter type coercion and validation
- Supported parameter types: `str`, `int`, `float`, `bool`
- Parameter `choices`, `min`, and `max` constraints
- `raw` and `c_string` template rendering
- Declarative runtime-argument contracts
- Optional per-method build-type constraints
- Resolved parameters stored in `build.json`
- Runtime-argument contract stored in `build.json`
- Stronger payload/build compatibility checks
- Standard-library regression tests

## Parameter precedence

Highest priority wins:

1. CLI `--set`
2. Preset `parameters`
3. Method parameter `default`

## Method contract example

```json
{
  "parameters": {
    "target_pid": {
      "type": "int",
      "required": true,
      "min": 1,
      "description": "Target process ID"
    },
    "module_name": {
      "type": "str",
      "required": false,
      "default": "example.exe",
      "render": "c_string"
    }
  },
  "runtime_arguments": [
    {
      "name": "address",
      "type": "hex",
      "required": true,
      "description": "Runtime address to inspect"
    }
  ]
}
```

A declared build-time parameter is referenced from a template with:

```text
{{PARAM_TARGET_PID}}
{{PARAM_MODULE_NAME}}
```

`render: "c_string"` escapes backslashes, quotes, tabs, and line breaks but
does not add surrounding quotation marks. The method template controls the
C/C++ syntax.

## CLI example

```bash
python3 mifa.py build \
  --preset example-x64 \
  --set target_pid=3988 \
  --set module_name=explorer.exe
```

## Test

```bash
python3 -m py_compile mifa.py core/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
```

Existing v1.0 methods do not need to add `parameters`, `runtime_arguments`, or
`build_types`; all three fields are optional and default to backward-compatible
behavior.

## End-to-end regression method

Batch 1 adds `parameter-test` so the parameter engine can be validated through
the normal Mifa CLI and compiler path.

```bash
python3 mifa.py build \
  --preset parameter-test-x64 \
  --set message="Phase 2 OK" \
  --set repeat=3 \
  --set enabled=true
```

The generated `build.json` should contain the resolved parameter values and the
declared runtime-argument contract.

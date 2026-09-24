# Mifa v2.0 Validation

## Release Inventory

~~~text
Version : 2.0.0
Methods : 45
Presets : 82
~~~

## Automated Gates

~~~bash
python3 -m py_compile mifa.py core/*.py tools/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
python3 tools/verify.py --strict

python3 tools/release_validate.py \
  --compile \
  --json dist/v2.0-release-validation.json
~~~

Expected full compile result:

~~~text
Methods  : 45/45 valid
Presets  : 82/82 valid
Compiled : 82
Failures : 0
~~~

## Runtime Validation

Windows runtime validation is tracked separately from cross-compilation.

`build-tested` does not imply runtime validation.

`runtime-tested` is reserved for generated Windows output that completes the
intended runtime check.

## Smoke Bundles

~~~bash
python3 tools/prepare_smoke.py --arch x64
python3 tools/prepare_smoke.py --arch x86
~~~

Expected paths:

~~~text
dist/v2.0-smoke-x64/
dist/v2.0-smoke-x86/
~~~

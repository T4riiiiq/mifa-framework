# Mifa v1.2.0 Release Notes

Mifa v1.2.0 completes Phase 3: Runtime and Payload Architecture.

## Payload architecture

Mifa now treats payload input as a first-class build object through Payload
Contract v2.

Supported adapters:

```text
raw
text
json
pe
```

Supported staging transforms:

```text
copy
base64
hex
```

Build manifests preserve separate source and staged provenance, including
size and SHA-256.

## Advanced method foundations

Six local inspection foundations were added:

```text
win32-payload-inspect
win32-file-buffer
win32-base64-buffer
win32-hex-buffer
win32-pe-runtime-info
win32-pe-section-characteristics
```

These methods are intentionally local inspection foundations. The buffer
decoders do not execute decoded content, and the PE inspection methods parse
file-backed data without loading the image for execution.

## Release tooling

The release validator now covers payload-required presets with deterministic
harmless fixtures, allowing the complete preset catalog to participate in the
compile matrix.

The curated smoke tool now builds 13 methods for either x64 or x86 and
generates:

- runtime fixture data
- a smoke manifest with SHA-256 hashes
- a PowerShell smoke runner
- one runtime result log

## Catalog

```text
34 methods
60 presets
30 Windows analysis/foundation methods
4 regression/test methods
```

## Validation

Before the v1.2.0 tag is created, the release candidate must pass:

- full Python syntax validation
- complete unit test suite
- 34/34 method contract validation
- 60/60 preset validation
- full x64/x86 compile matrix
- curated 13-method x64 Windows runtime smoke
- curated 13-method x86 Windows runtime smoke
- strict clean-tree release validation

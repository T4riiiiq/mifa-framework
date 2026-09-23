# Phase 3 — Batch 1: Runtime & Payload Architecture

Batch 1 promotes payload input from a copied file into a first-class Mifa
build object with an explicit contract, typed validation, transformation
metadata, and source/staged provenance.

## Payload Contract v2

Methods may define an optional `payload_contract`:

```json
{
  "payload_contract": {
    "required": true,
    "types": ["raw", "text", "json", "pe"],
    "transforms": ["copy", "base64", "hex"],
    "default_transform": "copy",
    "min_size_bytes": 1,
    "max_size_bytes": 16777216
  }
}
```

For backward compatibility, methods without `payload_contract` continue to use
`requires_payload` and `payload_types` and implicitly support only `copy`.

When a v2 contract is present, its `required` and `types` values must match the
legacy fields. This keeps old tooling and contracts deterministic during the
migration.

## Built-in input adapters

The v2 payload manager supports four non-executing validation adapters:

- `raw`: any non-empty bytes within the method size limits
- `text`: valid UTF-8
- `json`: valid UTF-8 JSON
- `pe`: input begins with the `MZ` signature

The adapters validate and stage inputs only. They do not execute payload
content.

## Staging transforms

Supported transforms are:

- `copy`: byte-for-byte staging
- `base64`: Base64 text representation
- `hex`: hexadecimal text representation

Transforms are build-time data transformations only. Mifa does not add a
runtime decoder or automatic execution path in this batch.

Select a transform with:

```bash
python3 mifa.py build \
  --preset payload-test-x64 \
  --payload ./sample.txt \
  --payload-type text \
  --payload-transform base64
```

If `--payload-transform` is omitted, the method contract's
`default_transform` is used.

## Provenance

`build.json` records both input and staged metadata:

```text
payload_contract
payload.type
payload.transform
payload.source.name
payload.source.suffix
payload.source.mime_type
payload.source.size_bytes
payload.source.sha256
payload.staged.file
payload.staged.name
payload.staged.size_bytes
payload.staged.sha256
```

The absolute source path is intentionally not written into `build.json`.

## Template tokens

Existing tokens remain compatible:

```text
{{PAYLOAD_NAME}}
{{PAYLOAD_TYPE}}
{{PAYLOAD_SIZE}}
{{PAYLOAD_SHA256}}
```

They continue to describe the staged input.

Payload Contract v2 additionally provides:

```text
{{PAYLOAD_TRANSFORM}}
{{PAYLOAD_SOURCE_NAME}}
{{PAYLOAD_SOURCE_SIZE}}
{{PAYLOAD_SOURCE_SHA256}}
{{PAYLOAD_STAGED_NAME}}
{{PAYLOAD_STAGED_SIZE}}
{{PAYLOAD_STAGED_SHA256}}
```

## Validation

Run:

```bash
python3 -m py_compile mifa.py core/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
```

Then perform a harmless end-to-end build:

```bash
printf 'Mifa Phase 3 payload test\n' > /tmp/mifa-payload-test.txt

python3 mifa.py build \
  --preset payload-test-x64 \
  --payload /tmp/mifa-payload-test.txt \
  --payload-type text \
  --payload-transform base64
```

Inspect the resulting `build.json` and verify that the source and staged
SHA-256 values are both present and that `payload.transform` is `base64`.

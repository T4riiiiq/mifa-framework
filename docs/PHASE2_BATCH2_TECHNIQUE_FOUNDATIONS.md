# Phase 2 — Batch 2: Technique Foundations

Batch 2 adds reusable Windows analysis foundations on top of the Phase 2
parameter engine.

## Added methods

| Method | Purpose |
|---|---|
| `win32-api-resolve` | Resolve and report a Win32 export address without invoking it |
| `win32-local-buffer` | Local RW allocation, initialization, RW -> R transition, inspection, release |
| `win32-local-thread` | Benign local worker-thread lifecycle |
| `win32-dll-load-info` | Map a DLL with `DONT_RESOLVE_DLL_REFERENCES` and report module information |
| `win32-file-map` | Read-only file mapping with bounded hex preview |
| `win32-runtime-helper` | Multi-source C++ helper architecture regression/foundation |

Each method includes x64 and x86 release presets.

## Scope

This batch deliberately stays at local-process and read-only inspection
primitives. It does not add remote process injection, executable-memory
payload runners, process hollowing, or security-control bypass logic.

## Parameter examples

```bash
python3 mifa.py build \
  --preset win32-local-buffer-x64 \
  --set buffer_size=8192 \
  --set fill_byte=90
```

```bash
python3 mifa.py build \
  --preset win32-local-thread-x64 \
  --set iterations=5 \
  --set delay_ms=100
```

```bash
python3 mifa.py build \
  --preset win32-file-map-x64 \
  --set preview_bytes=32
```

## Runtime examples

After transferring the compiled binaries to a Windows lab:

```text
win32-api-resolve.exe kernel32.dll GetCurrentProcessId
win32-dll-load-info.exe C:\Windows\System32\version.dll
win32-file-map.exe C:\Windows\System32\notepad.exe
win32-runtime-helper.exe lab-test
```

## Validation

```bash
python3 -m py_compile mifa.py core/*.py
python3 -m unittest discover -s tests -v
python3 mifa.py check
```

With Batch 1 plus Batch 2 installed, the expected method catalog size is:

```text
28 methods checked
28 valid
0 invalid
```

The Batch 2 test module also verifies that all six contracts are valid, all
declared templates exist, both x64/x86 presets exist, and the Batch 2
templates do not contain remote-execution primitives.

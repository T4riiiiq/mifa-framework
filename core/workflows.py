QUICK_ENTRIES = [
    {"alias": "native", "method": "win32-local-thread", "category": "Techniques", "description": "Native local thread lifecycle"},
    {"alias": "peinfo", "method": "win32-pe-runtime-info", "category": "PE / Runtime", "description": "Inspect PE runtime metadata"},
    {"alias": "sections", "method": "win32-pe-section-characteristics", "category": "PE / Runtime", "description": "Inspect PE section characteristics"},
    {"alias": "filebuf", "method": "win32-file-buffer", "category": "Buffers", "description": "Read a file into a local data buffer"},
    {"alias": "b64", "method": "win32-base64-buffer", "category": "Buffers", "description": "Decode Base64 into a local data buffer"},
    {"alias": "hex", "method": "win32-hex-buffer", "category": "Buffers", "description": "Decode hex into a local data buffer"},
    {"alias": "payload", "method": "win32-payload-inspect", "category": "Payload", "description": "Inspect Payload Contract metadata"},
    {"alias": "proc", "method": "win32-process-info", "category": "Process", "description": "Current process and host information"},
    {"alias": "procs", "method": "win32-process-enum", "category": "Process", "description": "Enumerate running processes"},
    {"alias": "threads", "method": "win32-thread-enum", "category": "Process", "description": "Enumerate threads for a PID"},
    {"alias": "modules", "method": "win32-module-enum", "category": "Modules", "description": "Enumerate loaded modules"},
    {"alias": "memmap", "method": "win32-memory-map", "category": "Memory", "description": "Enumerate virtual-memory regions"},
    {"alias": "mem", "method": "win32-memory-region", "category": "Memory", "description": "Inspect one virtual-memory region"},
    {"alias": "api", "method": "win32-api-resolve", "category": "Runtime", "description": "Resolve a Win32 export address"},
    {"alias": "filemap", "method": "win32-file-map", "category": "Runtime", "description": "Read-only file mapping preview"},
]


def alias_map():
    return {entry["alias"]: entry["method"] for entry in QUICK_ENTRIES}


def resolve_target(target, catalog):
    if target is None:
        return None
    method_id = alias_map().get(target, target)
    if catalog.get(method_id) is None:
        return None
    return method_id


def find_preset(store, method_id, architecture):
    matches = [
        preset for preset in store.discover()
        if preset.get("method") == method_id
        and preset.get("architecture") == architecture
    ]
    if not matches:
        return None
    release = [p for p in matches if p.get("build_type", "release") == "release"]
    selected = release or matches
    return sorted(selected, key=lambda item: item.get("id", ""))[0]

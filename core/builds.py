from pathlib import Path
from datetime import datetime, timezone
import json
import re


class BuildManager:
    def __init__(self, builds_dir: Path):
        self.builds_dir = builds_dir
        self.builds_dir.mkdir(parents=True, exist_ok=True)

    def _next_build_id(self):
        pattern = re.compile(r"^K-(\d{4})$")
        highest = 0

        for path in self.builds_dir.iterdir():
            if not path.is_dir():
                continue

            match = pattern.match(path.name)

            if match:
                number = int(match.group(1))
                highest = max(highest, number)

        return f"K-{highest + 1:04d}"

    def create(self, method, preset):
        build_id = self._next_build_id()
        build_dir = self.builds_dir / build_id

        source_dir = build_dir / "source"
        output_dir = build_dir / "output"

        source_dir.mkdir(parents=True)
        output_dir.mkdir(parents=True)

        build_data = {
            "build_id": build_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "created",

            "method": {
                "id": method.get("id"),
                "name": method.get("name"),
                "language": method.get("language"),
            },

            "preset": {
                "id": preset.get("id"),
                "architecture": preset.get("architecture"),
                "build_type": preset.get("build_type"),
            }
        }

        build_file = build_dir / "build.json"

        with build_file.open("w", encoding="utf-8") as f:
            json.dump(build_data, f, indent=4)

        return build_id, build_dir

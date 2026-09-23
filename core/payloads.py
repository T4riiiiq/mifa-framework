from pathlib import Path
import hashlib
import shutil


class PayloadManager:
    def _sha256(self, path: Path):
        digest = hashlib.sha256()

        with path.open("rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    def prepare(self, payload_path: Path, build_dir: Path):
        payload_path = payload_path.expanduser().resolve()

        if not payload_path.exists():
            raise FileNotFoundError(
                f"Payload not found: {payload_path}"
            )

        if not payload_path.is_file():
            raise ValueError(
                f"Payload is not a file: {payload_path}"
            )

        size = payload_path.stat().st_size

        if size == 0:
            raise ValueError(
                "Payload file is empty"
            )

        input_dir = build_dir / "input"

        input_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            input_dir / payload_path.name
        )

        shutil.copy2(
            payload_path,
            destination
        )

        return {
            "original": str(payload_path),
            "file": str(
                destination.relative_to(
                    build_dir
                )
            ),
            "name": payload_path.name,
            "size_bytes": size,
            "sha256": self._sha256(
                destination
            )
        }

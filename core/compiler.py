from pathlib import Path
import shutil
import subprocess


class Compiler:
    COMPILERS = {
        ("c", "x64"): "x86_64-w64-mingw32-gcc",
        ("c", "x86"): "i686-w64-mingw32-gcc",
    }

    def compile(self, method, preset, source_path: Path, build_dir: Path):
        language = method.get("language")
        architecture = preset.get("architecture")
        build_type = preset.get("build_type", "release")

        compiler_name = self.COMPILERS.get(
            (language, architecture)
        )

        if compiler_name is None:
            raise ValueError(
                f"No compiler configured for "
                f"{language}/{architecture}"
            )

        compiler_path = shutil.which(compiler_name)

        if compiler_path is None:
            raise RuntimeError(
                f"Compiler not found: {compiler_name}"
            )

        output_dir = build_dir / "output"
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_name = method.get(
            "output_name",
            "output.exe"
        )

        output_path = output_dir / output_name

        command = [
            compiler_path,
            str(source_path),
            "-o",
            str(output_path)
        ]

        if build_type == "release":
            command.extend([
                "-O2"
            ])

        elif build_type == "debug":
            command.extend([
                "-O0",
                "-g"
            ])

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Compilation failed"
            )

        if not output_path.exists():
            raise RuntimeError(
                "Compiler exited successfully "
                "but output file was not created"
            )

        return {
            "compiler": compiler_name,
            "command": command,
            "output": output_path,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

from pathlib import Path


class SourceGenerator:
    def _render(
        self,
        template,
        values
    ):
        generated = template

        for key, value in values.items():
            generated = generated.replace(
                key,
                str(value)
            )

        return generated

    def generate(
        self,
        method,
        preset,
        build_id,
        build_dir,
        payload_info=None,
        payload_type=None
    ):
        method_path = Path(
            method["_path"]
        )

        values = {
            "{{BUILD_ID}}":
                build_id,

            "{{ARCH}}":
                preset.get(
                    "architecture",
                    ""
                ),

            "{{BUILD_TYPE}}":
                preset.get(
                    "build_type",
                    ""
                ),

            "{{PAYLOAD_NAME}}":
                "",

            "{{PAYLOAD_TYPE}}":
                "",

            "{{PAYLOAD_SIZE}}":
                "",

            "{{PAYLOAD_SHA256}}":
                ""
        }

        if payload_info is not None:
            values.update({
                "{{PAYLOAD_NAME}}":
                    payload_info.get(
                        "name",
                        ""
                    ),

                "{{PAYLOAD_TYPE}}":
                    payload_type or "",

                "{{PAYLOAD_SIZE}}":
                    str(
                        payload_info.get(
                            "size_bytes",
                            ""
                        )
                    ),

                "{{PAYLOAD_SHA256}}":
                    payload_info.get(
                        "sha256",
                        ""
                    )
            })

        source_dir = (
            build_dir / "source"
        )

        source_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        generated_files = []

        for source in method.get(
            "sources",
            []
        ):
            template_path = (
                method_path
                / source["template"]
            )

            if not template_path.exists():
                raise FileNotFoundError(
                    f"Template not found: "
                    f"{template_path}"
                )

            template = (
                template_path.read_text(
                    encoding="utf-8"
                )
            )

            generated = self._render(
                template,
                values
            )

            output_path = (
                source_dir
                / source["output"]
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            output_path.write_text(
                generated,
                encoding="utf-8"
            )

            generated_files.append({
                "path": output_path,
                "compile": source[
                    "compile"
                ]
            })

        return generated_files

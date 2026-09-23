from pathlib import Path


class SourceGenerator:
    def generate(
        self,
        method,
        preset,
        build_id,
        build_dir,
        payload_info=None,
        payload_type=None
    ):
        method_path = Path(method["_path"])

        template_relative = method.get("template")
        source_name = method.get("source_name")

        if not template_relative:
            raise ValueError(
                f"Method '{method.get('id')}' "
                "does not define a template"
            )

        if not source_name:
            raise ValueError(
                f"Method '{method.get('id')}' "
                "does not define source_name"
            )

        template_path = (
            method_path / template_relative
        )

        if not template_path.exists():
            raise FileNotFoundError(
                f"Template not found: "
                f"{template_path}"
            )

        template = template_path.read_text(
            encoding="utf-8"
        )

        values = {
            "{{BUILD_ID}}": build_id,
            "{{ARCH}}": preset.get(
                "architecture",
                ""
            ),
            "{{BUILD_TYPE}}": preset.get(
                "build_type",
                ""
            ),

            "{{PAYLOAD_NAME}}": "",
            "{{PAYLOAD_TYPE}}": "",
            "{{PAYLOAD_SIZE}}": "",
            "{{PAYLOAD_SHA256}}": ""
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

        generated = template

        for key, value in values.items():
            generated = generated.replace(
                key,
                str(value)
            )

        source_dir = (
            build_dir / "source"
        )

        source_path = (
            source_dir / source_name
        )

        source_path.write_text(
            generated,
            encoding="utf-8"
        )

        return source_path

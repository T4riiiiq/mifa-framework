class MethodSchemaValidator:
    REQUIRED_FIELDS = [
        "id",
        "name",
        "language",
        "architectures",
        "requires_payload",
        "payload_types",
        "template",
        "source_name",
        "output_name"
    ]

    SUPPORTED_ARCHITECTURES = {
        "x64",
        "x86"
    }

    SUPPORTED_LANGUAGES = {
        "c"
    }

    def validate(self, method):
        errors = []

        for field in self.REQUIRED_FIELDS:
            if field not in method:
                errors.append(
                    f"Missing required field: {field}"
                )

        if errors:
            return errors

        method_id = method.get("id")

        if not isinstance(method_id, str) or not method_id.strip():
            errors.append(
                "id must be a non-empty string"
            )

        language = method.get("language")

        if language not in self.SUPPORTED_LANGUAGES:
            errors.append(
                f"Unsupported language: {language}"
            )

        architectures = method.get(
            "architectures"
        )

        if not isinstance(architectures, list):
            errors.append(
                "architectures must be a list"
            )

        elif not architectures:
            errors.append(
                "architectures must contain at least one architecture"
            )

        else:
            for architecture in architectures:
                if architecture not in self.SUPPORTED_ARCHITECTURES:
                    errors.append(
                        f"Unsupported architecture: {architecture}"
                    )

        requires_payload = method.get(
            "requires_payload"
        )

        if not isinstance(
            requires_payload,
            bool
        ):
            errors.append(
                "requires_payload must be true or false"
            )

        payload_types = method.get(
            "payload_types"
        )

        if not isinstance(payload_types, list):
            errors.append(
                "payload_types must be a list"
            )

        else:
            if (
                requires_payload is True
                and not payload_types
            ):
                errors.append(
                    "requires_payload=true but payload_types is empty"
                )

            if (
                requires_payload is False
                and payload_types
            ):
                errors.append(
                    "requires_payload=false but payload_types is not empty"
                )

        template = method.get(
            "template"
        )

        if not isinstance(
            template,
            str
        ) or not template.strip():
            errors.append(
                "template must be a non-empty string"
            )

        source_name = method.get(
            "source_name"
        )

        if not isinstance(
            source_name,
            str
        ) or not source_name.strip():
            errors.append(
                "source_name must be a non-empty string"
            )

        output_name = method.get(
            "output_name"
        )

        if not isinstance(
            output_name,
            str
        ) or not output_name.strip():
            errors.append(
                "output_name must be a non-empty string"
            )

        return errors

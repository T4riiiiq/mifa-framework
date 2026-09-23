class CompatibilityChecker:
    def validate(
        self,
        method,
        preset,
        payload_path=None,
        payload_type=None
    ):
        errors = []

        architecture = preset.get(
            "architecture"
        )

        supported_arch = method.get(
            "architectures",
            []
        )

        if architecture not in supported_arch:
            errors.append(
                f"Architecture '{architecture}' "
                f"is not supported by method "
                f"'{method.get('id')}'"
            )

        requires_payload = method.get(
            "requires_payload",
            False
        )

        accepted_payload_types = method.get(
            "payload_types",
            []
        )

        if requires_payload and payload_path is None:
            errors.append(
                "This method requires a payload"
            )

        if not requires_payload and payload_path is not None:
            errors.append(
                "This method does not accept a payload"
            )

        if payload_path is not None:
            if payload_type is None:
                errors.append(
                    "Payload type must be specified"
                )

            elif payload_type not in accepted_payload_types:
                errors.append(
                    f"Payload type '{payload_type}' "
                    f"is not supported by method "
                    f"'{method.get('id')}'"
                )

        return errors

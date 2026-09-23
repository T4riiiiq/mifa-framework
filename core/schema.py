import re


class MethodSchemaValidator:
    REQUIRED_FIELDS = [
        "id",
        "name",
        "language",
        "architectures",
        "requires_payload",
        "payload_types",
        "sources",
        "output_name"
    ]

    SUPPORTED_ARCHITECTURES = {
        "x64",
        "x86"
    }

    SUPPORTED_LANGUAGES = {
        "c",
        "cpp"
    }

    SUPPORTED_BUILD_TYPES = {
        "release",
        "debug"
    }

    SUPPORTED_PARAMETER_TYPES = {
        "str",
        "int",
        "float",
        "bool"
    }

    SUPPORTED_PARAMETER_RENDERERS = {
        "raw",
        "c_string"
    }

    SUPPORTED_RUNTIME_ARGUMENT_TYPES = {
        "str",
        "int",
        "float",
        "bool",
        "hex",
        "path"
    }

    PARAMETER_NAME = re.compile(
        r"^[A-Za-z_][A-Za-z0-9_]*$"
    )

    def _validate_parameters(
        self,
        method,
        errors
    ):
        parameters = method.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):
            errors.append(
                "parameters must be an object"
            )
            return

        for name, spec in parameters.items():
            prefix = (
                f"parameters.{name}"
            )

            if (
                not isinstance(
                    name,
                    str
                )
                or not self.PARAMETER_NAME.match(
                    name
                )
            ):
                errors.append(
                    f"Invalid parameter name: "
                    f"{name}"
                )
                continue

            if not isinstance(
                spec,
                dict
            ):
                errors.append(
                    f"{prefix} must be an object"
                )
                continue

            parameter_type = spec.get(
                "type",
                "str"
            )

            if (
                parameter_type
                not in self.SUPPORTED_PARAMETER_TYPES
            ):
                errors.append(
                    f"{prefix}.type is unsupported: "
                    f"{parameter_type}"
                )

            required = spec.get(
                "required",
                False
            )

            if not isinstance(
                required,
                bool
            ):
                errors.append(
                    f"{prefix}.required must be "
                    "true or false"
                )

            render = spec.get(
                "render",
                "raw"
            )

            if (
                render
                not in self.SUPPORTED_PARAMETER_RENDERERS
            ):
                errors.append(
                    f"{prefix}.render is unsupported: "
                    f"{render}"
                )

            description = spec.get(
                "description"
            )

            if (
                description is not None
                and not isinstance(
                    description,
                    str
                )
            ):
                errors.append(
                    f"{prefix}.description must "
                    "be a string"
                )

            choices = spec.get(
                "choices"
            )

            if (
                choices is not None
                and (
                    not isinstance(
                        choices,
                        list
                    )
                    or not choices
                )
            ):
                errors.append(
                    f"{prefix}.choices must be "
                    "a non-empty list"
                )

            minimum = spec.get(
                "min"
            )

            maximum = spec.get(
                "max"
            )

            if (
                minimum is not None
                and not isinstance(
                    minimum,
                    (
                        int,
                        float
                    )
                )
            ):
                errors.append(
                    f"{prefix}.min must be numeric"
                )

            if (
                maximum is not None
                and not isinstance(
                    maximum,
                    (
                        int,
                        float
                    )
                )
            ):
                errors.append(
                    f"{prefix}.max must be numeric"
                )

            if (
                isinstance(
                    minimum,
                    (
                        int,
                        float
                    )
                )
                and isinstance(
                    maximum,
                    (
                        int,
                        float
                    )
                )
                and minimum > maximum
            ):
                errors.append(
                    f"{prefix}.min cannot be "
                    "greater than max"
                )

    def _validate_runtime_arguments(
        self,
        method,
        errors
    ):
        runtime_arguments = method.get(
            "runtime_arguments",
            []
        )

        if not isinstance(
            runtime_arguments,
            list
        ):
            errors.append(
                "runtime_arguments must be a list"
            )
            return

        names = set()

        for index, argument in enumerate(
            runtime_arguments
        ):
            prefix = (
                f"runtime_arguments[{index}]"
            )

            if not isinstance(
                argument,
                dict
            ):
                errors.append(
                    f"{prefix} must be an object"
                )
                continue

            name = argument.get(
                "name"
            )

            if (
                not isinstance(
                    name,
                    str
                )
                or not name.strip()
            ):
                errors.append(
                    f"{prefix}.name must be a "
                    "non-empty string"
                )

            elif name in names:
                errors.append(
                    f"Duplicate runtime argument: "
                    f"{name}"
                )

            else:
                names.add(
                    name
                )

            argument_type = argument.get(
                "type",
                "str"
            )

            if (
                argument_type
                not in self.SUPPORTED_RUNTIME_ARGUMENT_TYPES
            ):
                errors.append(
                    f"{prefix}.type is unsupported: "
                    f"{argument_type}"
                )

            required = argument.get(
                "required",
                True
            )

            if not isinstance(
                required,
                bool
            ):
                errors.append(
                    f"{prefix}.required must be "
                    "true or false"
                )

            description = argument.get(
                "description"
            )

            if (
                description is not None
                and not isinstance(
                    description,
                    str
                )
            ):
                errors.append(
                    f"{prefix}.description must "
                    "be a string"
                )

    def _validate_build_types(
        self,
        method,
        errors
    ):
        build_types = method.get(
            "build_types"
        )

        if build_types is None:
            return

        if not isinstance(
            build_types,
            list
        ):
            errors.append(
                "build_types must be a list"
            )
            return

        if not build_types:
            errors.append(
                "build_types must contain at "
                "least one build type"
            )
            return

        for build_type in build_types:
            if (
                build_type
                not in self.SUPPORTED_BUILD_TYPES
            ):
                errors.append(
                    f"Unsupported build type: "
                    f"{build_type}"
                )

    def validate(self, method):
        errors = []

        for field in self.REQUIRED_FIELDS:
            if field not in method:
                errors.append(
                    f"Missing required field: {field}"
                )

        if errors:
            return errors

        method_id = method.get(
            "id"
        )

        if (
            not isinstance(
                method_id,
                str
            )
            or not method_id.strip()
        ):
            errors.append(
                "id must be a non-empty string"
            )

        name = method.get(
            "name"
        )

        if (
            not isinstance(
                name,
                str
            )
            or not name.strip()
        ):
            errors.append(
                "name must be a non-empty string"
            )

        language = method.get(
            "language"
        )

        if (
            language
            not in self.SUPPORTED_LANGUAGES
        ):
            errors.append(
                f"Unsupported language: "
                f"{language}"
            )

        architectures = method.get(
            "architectures"
        )

        if not isinstance(
            architectures,
            list
        ):
            errors.append(
                "architectures must be a list"
            )

        elif not architectures:
            errors.append(
                "architectures must contain at "
                "least one architecture"
            )

        else:
            for architecture in architectures:
                if (
                    architecture
                    not in self.SUPPORTED_ARCHITECTURES
                ):
                    errors.append(
                        f"Unsupported architecture: "
                        f"{architecture}"
                    )

        requires_payload = method.get(
            "requires_payload"
        )

        if not isinstance(
            requires_payload,
            bool
        ):
            errors.append(
                "requires_payload must be "
                "true or false"
            )

        payload_types = method.get(
            "payload_types"
        )

        if not isinstance(
            payload_types,
            list
        ):
            errors.append(
                "payload_types must be a list"
            )

        else:
            if (
                requires_payload is True
                and not payload_types
            ):
                errors.append(
                    "requires_payload=true but "
                    "payload_types is empty"
                )

            if (
                requires_payload is False
                and payload_types
            ):
                errors.append(
                    "requires_payload=false but "
                    "payload_types is not empty"
                )

        sources = method.get(
            "sources"
        )

        if not isinstance(
            sources,
            list
        ):
            errors.append(
                "sources must be a list"
            )

        elif not sources:
            errors.append(
                "sources must contain at "
                "least one file"
            )

        else:
            outputs = set()
            compile_count = 0

            for index, source in enumerate(
                sources
            ):
                prefix = (
                    f"sources[{index}]"
                )

                if not isinstance(
                    source,
                    dict
                ):
                    errors.append(
                        f"{prefix} must be "
                        "an object"
                    )
                    continue

                template = source.get(
                    "template"
                )

                output = source.get(
                    "output"
                )

                compile_file = source.get(
                    "compile"
                )

                if (
                    not isinstance(
                        template,
                        str
                    )
                    or not template.strip()
                ):
                    errors.append(
                        f"{prefix}.template must "
                        "be a non-empty string"
                    )

                if (
                    not isinstance(
                        output,
                        str
                    )
                    or not output.strip()
                ):
                    errors.append(
                        f"{prefix}.output must "
                        "be a non-empty string"
                    )

                elif output in outputs:
                    errors.append(
                        f"Duplicate source output: "
                        f"{output}"
                    )

                else:
                    outputs.add(
                        output
                    )

                if not isinstance(
                    compile_file,
                    bool
                ):
                    errors.append(
                        f"{prefix}.compile must "
                        "be true or false"
                    )

                elif compile_file:
                    compile_count += 1

            if compile_count == 0:
                errors.append(
                    "At least one source must "
                    "have compile=true"
                )

        output_name = method.get(
            "output_name"
        )

        if (
            not isinstance(
                output_name,
                str
            )
            or not output_name.strip()
        ):
            errors.append(
                "output_name must be a "
                "non-empty string"
            )

        self._validate_parameters(
            method,
            errors
        )

        self._validate_runtime_arguments(
            method,
            errors
        )

        self._validate_build_types(
            method,
            errors
        )

        return errors

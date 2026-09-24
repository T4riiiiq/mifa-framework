import unittest

from core.schema import MethodSchemaValidator


class SchemaTests(
    unittest.TestCase
):
    def setUp(self):
        self.schema = (
            MethodSchemaValidator()
        )

        self.method = {
            "id": "test",
            "name": "Test",
            "language": "cpp",
            "architectures": [
                "x64"
            ],
            "requires_payload": False,
            "payload_types": [],
            "sources": [
                {
                    "template": "templates/main.cpp.tmpl",
                    "output": "main.cpp",
                    "compile": True
                }
            ],
            "output_name": "test.exe",
            "parameters": {
                "count": {
                    "type": "int",
                    "required": False,
                    "default": 1,
                    "min": 1,
                    "max": 5
                }
            },
            "runtime_arguments": [
                {
                    "name": "pid",
                    "type": "int",
                    "required": True
                }
            ]
        }

    def test_extended_contract_valid(
        self
    ):
        self.assertEqual(
            self.schema.validate(
                self.method
            ),
            []
        )

    def test_duplicate_runtime_argument_rejected(
        self
    ):
        self.method[
            "runtime_arguments"
        ].append({
            "name": "pid",
            "type": "int",
            "required": False
        })

        errors = (
            self.schema.validate(
                self.method
            )
        )

        self.assertTrue(
            any(
                "Duplicate runtime argument"
                in error
                for error in errors
            )
        )

    def test_invalid_renderer_rejected(
        self
    ):
        self.method[
            "parameters"
        ][
            "count"
        ][
            "render"
        ] = "invalid"

        errors = (
            self.schema.validate(
                self.method
            )
        )

        self.assertTrue(
            any(
                "render is unsupported"
                in error
                for error in errors
            )
        )


    def test_optional_technique_contract_valid(
        self
    ):
        self.method["technique"] = {
            "alias": "example",
            "category": "Process / Memory",
            "role": "technique",
            "quick": True,
            "runtime": "native",
            "privilege": "user",
            "validation": "planned"
        }

        self.assertEqual(
            self.schema.validate(
                self.method
            ),
            []
        )

    def test_invalid_technique_role_rejected(
        self
    ):
        self.method["technique"] = {
            "alias": "example",
            "category": "Process / Memory",
            "role": "invalid",
            "quick": True,
            "runtime": "native",
            "privilege": "user",
            "validation": "planned"
        }

        errors = self.schema.validate(
            self.method
        )

        self.assertTrue(
            any(
                "Unsupported technique role"
                in error
                for error in errors
            )
        )

    def test_technique_contract_remains_optional(
        self
    ):
        self.assertNotIn(
            "technique",
            self.method
        )

        self.assertEqual(
            self.schema.validate(
                self.method
            ),
            []
        )


if __name__ == "__main__":
    unittest.main()

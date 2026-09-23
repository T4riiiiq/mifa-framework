import unittest

from core.compatibility import CompatibilityChecker


class CompatibilityTests(
    unittest.TestCase
):
    def setUp(self):
        self.checker = (
            CompatibilityChecker()
        )

        self.method = {
            "id": "test",
            "architectures": [
                "x64"
            ],
            "requires_payload": False,
            "payload_types": [],
            "build_types": [
                "release"
            ]
        }

        self.preset = {
            "architecture": "x64",
            "build_type": "release"
        }

    def test_valid_preset(
        self
    ):
        self.assertEqual(
            self.checker.validate_preset(
                self.method,
                self.preset
            ),
            []
        )

    def test_payload_type_without_payload_rejected(
        self
    ):
        errors = (
            self.checker.validate(
                self.method,
                self.preset,
                payload_type="raw"
            )
        )

        self.assertTrue(
            any(
                "without a payload"
                in error
                for error in errors
            )
        )

    def test_method_build_type_constraint(
        self
    ):
        preset = {
            "architecture": "x64",
            "build_type": "debug"
        }

        errors = (
            self.checker.validate_preset(
                self.method,
                preset
            )
        )

        self.assertTrue(
            any(
                "not supported by method"
                in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()

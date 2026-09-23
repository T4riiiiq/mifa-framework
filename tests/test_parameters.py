import unittest

from core.parameters import ParameterResolver


class ParameterResolverTests(
    unittest.TestCase
):
    def setUp(self):
        self.resolver = (
            ParameterResolver()
        )

        self.method = {
            "parameters": {
                "message": {
                    "type": "str",
                    "required": True,
                    "default": "hello",
                    "render": "c_string"
                },
                "repeat": {
                    "type": "int",
                    "required": False,
                    "default": 1,
                    "min": 1,
                    "max": 5
                },
                "enabled": {
                    "type": "bool",
                    "required": False,
                    "default": True
                }
            }
        }

        self.preset = {
            "parameters": {
                "repeat": 2
            }
        }

    def test_defaults_preset_and_cli_precedence(
        self
    ):
        values, errors = (
            self.resolver.resolve(
                self.method,
                self.preset,
                [
                    "message=world",
                    "repeat=0x3",
                    "enabled=false"
                ]
            )
        )

        self.assertEqual(
            errors,
            []
        )

        self.assertEqual(
            values["message"],
            "world"
        )

        self.assertEqual(
            values["repeat"],
            3
        )

        self.assertFalse(
            values["enabled"]
        )

    def test_unknown_parameter_rejected(
        self
    ):
        _, errors = (
            self.resolver.resolve(
                self.method,
                self.preset,
                [
                    "unknown=value"
                ]
            )
        )

        self.assertTrue(
            any(
                "Unknown parameter"
                in error
                for error in errors
            )
        )

    def test_range_validation(
        self
    ):
        _, errors = (
            self.resolver.resolve(
                self.method,
                self.preset,
                [
                    "repeat=99"
                ]
            )
        )

        self.assertTrue(
            any(
                "<= 5"
                in error
                for error in errors
            )
        )

    def test_duplicate_cli_parameter_rejected(
        self
    ):
        _, errors = (
            self.resolver.resolve(
                self.method,
                self.preset,
                [
                    "repeat=2",
                    "repeat=3"
                ]
            )
        )

        self.assertTrue(
            any(
                "more than once"
                in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()

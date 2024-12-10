import unittest
from unittest.mock import patch, Mock, MagicMock
from src.tools import swagger_reader


class TestGetApiSpecByPath(unittest.TestCase):
    @patch("src.tools.swagger_reader.SwaggerAPIReader")
    def test_get_api_spec_by_path(self, MockSwaggerAPIReader):
        test_cases = [
            {
                "name": "test case 1: valid api path",
                "api_path": "/valid/path",
                "expected_result": '{"valid": "spec"}',
                "mock_return_value": Mock(
                    full_spec_in_json=Mock(return_value='{"valid": "spec"}')
                ),
            },
            {
                "name": "test case 2: invalid api path",
                "api_path": "/invalid/path",
                "expected_result": "{}",
                "mock_return_value": Mock(full_spec_in_json=Mock(return_value="{}")),
            },
            {
                "name": "test case 3: empty api path",
                "api_path": "",
                "expected_result": "{}",
                "mock_return_value": Mock(full_spec_in_json=Mock(return_value="{}")),
            },
        ]

        for test in test_cases:
            with self.subTest(test["name"]):
                MockSwaggerAPIReader.return_value.get_endpoint.return_value = test[
                    "mock_return_value"
                ]
                result = swagger_reader.get_api_spec_by_path(test["api_path"])
                self.assertEqual(result, test["expected_result"])


class TestGetApiSpec(unittest.TestCase):
    @patch("src.tools.swagger_reader.SwaggerAPIReader")
    def test_get_api_spec(self, mock_reader):
        # Arrange
        test_cases = [
            {
                "name": "Test Case 1",
                "input": "/get",
                "expected": '{"path": "/get", "description": "Returns a list of users"}',
                "mock_return": MagicMock(
                    full_spec_in_json=MagicMock(
                        return_value='{"path": "/get", "description": "Returns a list of users"}'
                    )
                ),
            },
            {
                "name": "Test Case 2",
                "input": "/get",
                "expected": '{"path": "/get", "description": "Returns a single user"}',
                "mock_return": MagicMock(
                    full_spec_in_json=MagicMock(
                        return_value='{"path": "/get", "description": "Returns a single user"}'
                    )
                ),
            },
        ]

        for test in test_cases:
            mock_reader.return_value.get_endpoint.return_value = test["mock_return"]

            # Act
            result = swagger_reader.get_api_spec()

            # Assert
            self.assertEqual(result, test["expected"], test["name"])


if __name__ == "__main__":
    unittest.main()

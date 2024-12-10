import os
import unittest
from unittest.mock import patch, Mock, MagicMock
from src.tools import swagger_reader
from urllib.parse import urlparse

from src.tools.swagger_reader import get_api_spec_by_path, SwaggerAPIReader

HTTPBIN_API_SPEC_URL = "https://httpbin.org/spec.json"


class TestGetApiSpecByPath(unittest.TestCase):
    @patch("src.tools.swagger_reader.SwaggerAPIReader")
    @patch("src.tools.swagger_reader.yaml")
    @patch("src.tools.swagger_reader.open", new_callable=MagicMock)
    def test_get_api_spec_by_path(self, mock_open, mock_yaml, mock_reader):
        # Setup
        api_path = "/api/path"
        expected_api_spec = {"api": "spec"}
        expected_api_spec_yaml = "api: spec"
        expected_filename = "httpbin_org_api_path.yaml"
        expected_file_path = f"./api-specs/{expected_filename}"
        expected_json_result = '{"api": "spec"}'

        mock_reader_instance = mock_reader.return_value
        mock_reader_instance.get_endpoint.return_value.full_spec.return_value = (
            expected_api_spec
        )
        mock_reader_instance.get_endpoint.return_value.full_spec_in_json.return_value = (
            expected_json_result
        )

        mock_yaml.dump.return_value = expected_api_spec_yaml

        # Call the function
        actual_result = get_api_spec_by_path(api_path)

        # Asserts
        mock_reader.assert_called_once_with(HTTPBIN_API_SPEC_URL)
        mock_reader_instance.get_endpoint.assert_called_once_with(api_path)
        mock_yaml.dump.assert_called_once_with(
            expected_api_spec, default_flow_style=False
        )
        mock_open.assert_called_once_with(expected_file_path, "w")
        mock_open.return_value.__enter__().write.assert_called_once_with(
            expected_api_spec_yaml
        )
        self.assertEqual(expected_json_result, actual_result)


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

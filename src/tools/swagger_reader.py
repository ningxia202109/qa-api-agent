import requests
import yaml
import os
from urllib.parse import urlparse

from typing import Dict, Optional
from src.models import ApiSpec

HTTPBIN_API_SPEC_URL = "https://httpbin.org/spec.json"


class SwaggerAPIReader:
    def __init__(self, swagger_url: str):
        self.swagger_url = swagger_url
        self.api_spec = None
        self.endpoints: Dict[str, ApiSpec] = {}
        if not self.api_spec:
            self.fetch_api_spec()

    def fetch_api_spec(self) -> None:
        """Fetch the Swagger API specification from the given URL."""
        response = requests.get(self.swagger_url)
        response.raise_for_status()
        self.api_spec = response.json()
        self._parse_endpoints()

    def _parse_endpoints(self) -> None:
        """Parse the API spec and create ApiSpec objects for each endpoint."""
        paths = self.api_spec.get("paths", {})
        for path, methods in paths.items():
            self.endpoints[path] = ApiSpec(path, methods)

    def get_api_info(self) -> Dict[str, str]:
        """Get basic information about the API."""
        if not self.api_spec:
            self.fetch_api_spec()

        info = self.api_spec.get("info", {})
        return {
            "title": info.get("title", "N/A"),
            "version": info.get("version", "N/A"),
            "description": info.get("description", "N/A"),
        }

    def get_endpoints(self) -> Dict[str, ApiSpec]:
        """Get all endpoints as ApiSpec objects."""
        if not self.api_spec:
            self.fetch_api_spec()
        return self.endpoints

    def get_endpoint(self, path: str) -> Optional[ApiSpec]:
        """Get a specific endpoint by path."""
        return self.endpoints.get(path)

    def print_api_summary(self) -> None:
        """Print a summary of the API including info and endpoints."""
        info = self.get_api_info()
        endpoints = self.get_endpoints()

        print("API Summary:")
        print(f"Title: {info['title']}")
        print(f"Version: {info['version']}")
        print(f"Description: {info['description']}")
        print("\nEndpoints:")
        for path, api_spec in endpoints.items():
            print(f"\n{path}")
            for method in api_spec.get_all_methods():
                http_method = api_spec.get_method(method)
                print(f"  {method.upper()}: {http_method.summary}")
                parameters = api_spec.get_parameters(method)
                if parameters:
                    print("    Parameters:")
                    for param in parameters:
                        print(
                            f"      - {param.get('name', 'N/A')} ({param.get('in', 'N/A')})"
                        )
                print("    Responses:")
                for status, response in http_method.responses.items():
                    print(f"      {status}: {response.get('description', 'N/A')}")


def get_api_spec() -> str:
    reader = SwaggerAPIReader(HTTPBIN_API_SPEC_URL)
    selected_api = "/get"
    selected_apiSpec = reader.get_endpoint(selected_api)
    return selected_apiSpec.full_spec_in_json()


def get_api_spec_by_path(api_path: str) -> str:
    reader = SwaggerAPIReader(HTTPBIN_API_SPEC_URL)
    api_spec = reader.get_endpoint(api_path)
    api_spec_yaml = yaml.dump(api_spec.full_spec(), default_flow_style=False)

    # Generate a filename based on the API path
    hostname = urlparse(HTTPBIN_API_SPEC_URL).hostname.replace(".", "_")
    api_path_filename = api_path.replace("/", "_").strip("_")
    filename = f"{hostname}_{api_path_filename}.yaml"
    file_path = os.path.join("./api-specs", filename)

    # Write the YAML to a file
    with open(file_path, "w") as file:
        file.write(api_spec_yaml)

    return api_spec.full_spec_in_json()

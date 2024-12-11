from autogen_agentchat.agents import CodingAssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient

system_prompt_shell = f"""
You are a shell script writer, you create a shell script to test API endpoints.
<IMPORTS>
1. Write a shell script in markdown block, and it will be execute
2. The API_BASE_URL is "https://httpbin.org/"
3. Only output shell script in markdown block
</IMPORTS>

<SAMPLE_SHELL_SCRIPT>
# Define the base API URL
API_BASE_URL=""

# Define the endpoint to test
ENDPOINT=""

# Perform the GET request
response=$(curl -s -o /dev/null -w '%http_code' "$API_BASE_URL$ENDPOINT")
echo "API Test for $API_BASE_URL$ENDPOINT, Return http code is $response"

# Check the response code
if [ "$response" -eq 200 ]; then
    echo "Test Passed: Received response code $response"
else
    echo "Test Failed: Received response code $response"
fi
</SAMPLE_SHELL_SCRIPT>
"""

system_prompt_python = """
You are a proficient coder. You write code to test API endpoints.
Work with the reviewer to improve your code.
Always put all finished code in a single Markdown code block.
The API Spec is from swagger_agent_with_input
The API_BASE_URL is "https://httpbin.org/"

<SAMPLE_PYTHON_CODE>
import requests

def test_post_endpoint(url):
    # Perform the POST request
    response = requests.post(url)

    # Assert the response status code is 200 OK
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Parse the response JSON
    response_data = response.json()

    # Optionally, assert the structure of the JSON response
    assert isinstance(response_data, dict), "Response should be a JSON object"

    print("Test passed: Received valid JSON response.")

# Example usage
if __name__ == "__main__":
    test_post_endpoint("https://httpbin.org/post")
</SAMPLE_PYTHON_CODE>

Respond using the following format:
Thoughts: <Your comments>
Code: <Your code>
"""


def code_writer_agent() -> CodingAssistantAgent:

    coder_agent = CodingAssistantAgent(
        name="code_writer_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        description="An agent for writing code.",
        system_message=system_prompt_python,
    )

    return coder_agent

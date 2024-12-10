from autogen_agentchat.agents import CodingAssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient

system_prompt = f"""
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


def code_writer_agent() -> CodingAssistantAgent:

    coder_agent = CodingAssistantAgent(
        name="code_writer_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        description="Write code based on the given prompt.",
        system_message=system_prompt,
    )

    def write_code_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.last_message())

    # Attach the method to the agent
    coder_agent.write_code_to_file = write_code_to_file.__get__(coder_agent)

    return coder_agent

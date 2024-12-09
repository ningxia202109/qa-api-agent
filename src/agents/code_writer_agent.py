from autogen_agentchat.agents import CodingAssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient

system_prompt = f"""
You are a shell script writer, you create a shell script to test API endpoints based on the given API spec. 
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

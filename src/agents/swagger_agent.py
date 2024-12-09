from src.tools import get_api_spec

from autogen_core.components.tools import FunctionTool
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_core.components.tools import FunctionTool
from autogen_agentchat.agents import ToolUseAssistantAgent

system_prompt = f"""
You are a helpful assistant that can read and understand Swagger API specifications. Your main responsibilities include:
you use tool to read and understand Swagger API specifications,

"""


def swagger_agent():
    swagger_agent = ToolUseAssistantAgent(
        name="swagger_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        registered_tools=[
            FunctionTool(
                get_api_spec,
                description="Query API spec info from swagger API. return api spec.",
            )
        ],
        description="Query API spec info from swagger API. return api spec in json format.",
        system_message=system_prompt,
    )
    return swagger_agent

from dataclasses import dataclass

from autogen_core.base import MessageContext, TopicId
from autogen_core.components import RoutedAgent, default_subscription, message_handler
from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.components.tools import FunctionTool
from autogen_core.base import AgentId, AgentInstantiationContext, MessageContext
from autogen_ext.models import OpenAIChatCompletionClient
from typing import Dict, List, Union
from typing import List

from autogen_core.components.tool_agent import ToolAgent, tool_agent_caller_loop
from autogen_core.components.tools import FunctionTool, Tool, ToolSchema

from autogen_agentchat.agents import CodingAssistantAgent, ToolUseAssistantAgent

from autogen_agentchat.task import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import Console


from src.tools import get_api_spec


system_prompt = f'''
You are a helpful assistant that can read and understand Swagger API specifications. Your main responsibilities include:
you use tool to read and understand Swagger API specifications,

'''

def swagger_agent():
    swagger_agent = ToolUseAssistantAgent(
        name="swagger_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        registered_tools=[FunctionTool(
        get_api_spec,
        description="Query API spec info from swagger API. return api spec.",
    )],
        description="Query API spec info from swagger API. return api spec in json format.",
        system_message=system_prompt,
    )
    return swagger_agent

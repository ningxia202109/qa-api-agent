from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient

system_prompt = """
You are a code reviewer. You focus on correctness, efficiency and safety of the code.
Respond with 'APPROVE' to when your feedbacks are addressed
Respond using the following JSON format:
{
    "correctness": "<Your comments>",
    "efficiency": "<Your comments>",
    "safety": "<Your comments>",
    "approval": "<APPROVE or REVISE>",
    "suggested_changes": "<Your comments>"
}
"""


def code_reviewer_agent() -> AssistantAgent:
    reviewer_agent = AssistantAgent(
        name="code_reviewer_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        description="Review code from code_writer_agent, provide feedback APPROVE or REVISE.",
        system_message=system_prompt,
    )
    return reviewer_agent

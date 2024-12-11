from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient

api_test_planner_prompt = """
You are a task planner. You plan a task to test an API endpoint.
You have following participants: 
- swagger_agent_with_input
- code_writer_agent
- code_reviewer_agent

You will do following steps:
1. Send a task message to swagger_agent_with_input
2. Send api spec from swagger_agent_with_input to code_writer_agent
3. Send test code from code_writer_agent to code_review_agent
4. Send feedback from code_review_agent to code_writer_agent
5. Repeat step 2, 3 and 4 until the feedback from code_review_agent is "APPROVE".
6. End with "TERMINATE" if feedback from code_review_agent is "APPROVE", 
"""


def test_plan_agent() -> AssistantAgent:
    reviewer_agent = AssistantAgent(
        name="test_plan_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        description="An agent for plan API test.",
        system_message=api_test_planner_prompt,
    )
    return reviewer_agent

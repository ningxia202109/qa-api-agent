from src.agents import (
    swagger_agent,
    code_writer_agent,
    code_executor_agent,
    code_reviewer_agent,
    test_plan_agent,
)


from autogen_agentchat.task import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import Console
from autogen_ext.code_executors import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models import OpenAIChatCompletionClient


async def group_chat(task_message) -> None:

    text_termination = TextMentionTermination("TERMINATE")
    max_message_termination = MaxMessageTermination(10)

    termination = text_termination | max_message_termination
    async with DockerCommandLineCodeExecutor(
        image="curlimages/curl", container_name="api-tester", work_dir="temp_scripts"
    ) as executor:

        swagger_agent_team = RoundRobinGroupChat(
            [
                swagger_agent.swagger_agent(),
                code_writer_agent.code_writer_agent(),
                code_executor_agent.code_executor_agent(executor),
            ],
            termination_condition=termination,
        )

        await Console(
            swagger_agent_team.run_stream(
                task=task_message
            )  # Sample task message is "query api spec from swagger."
        )


async def swagger_tool(task_message) -> None:

    swagger_agent_team = RoundRobinGroupChat(
        [swagger_agent.swagger_agent_with_input()],
        termination_condition=MaxMessageTermination(2),
    )
    await Console(swagger_agent_team.run_stream(task=task_message))


async def create_test_code() -> None:

    text_termination = TextMentionTermination("APPROVE")
    max_message_termination = MaxMessageTermination(5)
    termination = text_termination | max_message_termination
    coder_team = RoundRobinGroupChat(
        [
            code_writer_agent.code_writer_agent(),
            code_reviewer_agent.code_reviewer_agent(),
        ],
        termination_condition=termination,
    )
    api_spec = TextMessage(
        content="""The API specification for the path `/post` is as follows:

### Summary
- **Description**: The request's POST parameters.

### Method
- **POST**

### Produces
- **Response Format**: `application/json`

### Responses
- **200**: 
  - **Description**: The request's POST parameters.

### Tags
- **HTTP Methods**

### Parameters
- **No parameters are defined for this request.** 

This indicates that the `/post` endpoint is designed to receive POST requests, and it will return a JSON response with a 200 status code when the request is successful.
""",
        source="swagger_agent_with_input",
    )
    await Console(coder_team.run_stream(task=api_spec))


async def api_test_task(task_message) -> None:
    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=15)
    termination = text_mention_termination | max_messages_termination

    api_test_team = SelectorGroupChat(
        [
            test_plan_agent.test_plan_agent(),
            swagger_agent.swagger_agent_with_input(),
            code_writer_agent.code_writer_agent(),
            code_reviewer_agent.code_reviewer_agent(),
        ],
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        termination_condition=termination,
    )
    await Console(api_test_team.run_stream(task=task_message))

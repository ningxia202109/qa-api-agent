from src.agents import swagger_agent, code_writer_agent, code_executor_agent

from autogen_agentchat.task import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import Console
from autogen_ext.code_executors import DockerCommandLineCodeExecutor


async def group_chat() -> None:

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
            swagger_agent_team.run_stream(task="query api spec from swagger.")
        )


async def swagger_tool() -> None:

    swagger_agent_team = RoundRobinGroupChat(
        [swagger_agent.swagger_agent_with_input()],
        termination_condition=MaxMessageTermination(2),
    )

    await Console(
        swagger_agent_team.run_stream(task="query api spec for api_path '/post'.")
    )

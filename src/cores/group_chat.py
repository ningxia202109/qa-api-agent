import src.agents as agents
import tempfile

from autogen_agentchat.task import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import Console
from autogen_ext.code_executors import DockerCommandLineCodeExecutor


async def group_chat():
    work_dir = tempfile.mkdtemp()

    text_termination = TextMentionTermination("TERMINATE")
    max_message_termination = MaxMessageTermination(10)

    termination = text_termination | max_message_termination
    async with DockerCommandLineCodeExecutor(
        image="curlimages/curl", container_name="api-tester", work_dir="temp_scripts"
    ) as executor:

        swagger_agent = agents.swagger_agent()
        code_writer_agent = agents.code_writer_agent()
        code_executor_agent = agents.code_executor_agent(executor)
        swagger_agent_team = RoundRobinGroupChat(
            [swagger_agent, code_writer_agent, code_executor_agent],
            termination_condition=termination,
        )

        await Console(
            swagger_agent_team.run_stream(task="query api spec from swagger.")
        )

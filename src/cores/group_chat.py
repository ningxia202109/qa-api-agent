import src.agents as agents

from autogen_agentchat.task import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import Console


async def group_chat():

    text_termination = TextMentionTermination("APPROVE")
    max_message_termination = MaxMessageTermination(5)

    termination = text_termination | max_message_termination
    swagger_agent = agents.swagger_agent()
    code_writer_agent = agents.code_writer_agent()
    swagger_agent_team = RoundRobinGroupChat(
        [swagger_agent, code_writer_agent],
        termination_condition=termination,
    )

    await Console(swagger_agent_team.run_stream(task="query api spec from swagger."))

from autogen_agentchat.agents import CodeExecutorAgent
from autogen_core.components.code_executor import CodeExecutor


def code_executor_agent(code_executor: CodeExecutor) -> CodeExecutorAgent:
    code_executor_agent = CodeExecutorAgent(
        "code_executor", code_executor=code_executor
    )
    return code_executor_agent

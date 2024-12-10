import asyncio
from src.cores import group_chat

task_message = "query api spec for api_path '/post'."
def main():
    asyncio.run(group_chat.swagger_tool(task_message))

if __name__ == "__main__":
    main()

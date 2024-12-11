import asyncio
from src.cores import group_chat

task_message = "query api spec for api_path '/post'."

def main():
    asyncio.run(group_chat.api_test_task(task_message))

if __name__ == "__main__":
    main()

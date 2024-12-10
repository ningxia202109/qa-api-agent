import asyncio
from src.cores import group_chat


def main():
    asyncio.run(group_chat.swagger_tool())

if __name__ == "__main__":
    main()

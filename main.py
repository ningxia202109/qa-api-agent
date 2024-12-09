import asyncio
from src.tools import get_api_spec
from src.agents import swagger_agent


def main():
    # print(get_api_spec())
    asyncio.run(swagger_agent())


if __name__ == "__main__":
    main()

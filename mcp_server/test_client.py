import asyncio

from mcp import Client
from mcp_server.server import mcp


async def main():

    async with Client(mcp) as client:

        result = await client.list_tools()

        print("Available MCP tools:")

        for tool in result.tools:
            print(f"- {tool.name}")

        print("\nCalling deployment_status...")

        tool_result = await client.call_tool(
            "deployment_status",
            {},
        )

        print("Tool result:")
        print(tool_result)


asyncio.run(main())
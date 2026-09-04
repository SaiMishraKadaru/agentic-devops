import asyncio
import sys

from mcp import Client, StdioServerParameters

from pathlib import Path


server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_server.server"],
    cwd=Path.cwd(),
)


async def main():

    async with Client(server_params) as client:

        result = await client.list_tools()

        print("Tools discovered from MCP Server:")

        for tool in result.tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")

        print("\nCalling deployment_status...")

        tool_result = await client.call_tool(
            "deployment_status",
            {},
        )

        print("\nTool result:")
        print(tool_result)


asyncio.run(main())
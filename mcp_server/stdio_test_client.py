import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


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

        print("\nget_container_status...")

        tool_result = await client.call_tool("get_container_status", {})

        print("\nTool result:")
        print(tool_result)

        print("\nget_container_logs...")

        tool_result = await client.call_tool("get_container_logs", {})

        print("\nTool result:")
        print(tool_result)


asyncio.run(main())
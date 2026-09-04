import asyncio
import os
import sys 
import json

from dotenv import load_dotenv
from google import genai
from mcp import Client, StdioServerParameters


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_server.server"],
)


def mcp_tools_to_gemini_tools(mcp_tools):

    gemini_tools = []

    for tool in mcp_tools:
        gemini_tools.append(
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            }
        )

    return gemini_tools


def mcp_result_to_text(tool_result):

    text_parts = []

    for content in tool_result.content:

        if hasattr(content, "text"):
            text_parts.append(content.text)

    return "\n".join(text_parts)


async def main():

    async with Client(server_params) as mcp_client:

        # Discover tools from MCP Server
        mcp_result = await mcp_client.list_tools()

        print("Tools discovered from MCP Server:")

        for tool in mcp_result.tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")

        # Convert MCP tools into Gemini tool definitions
        gemini_tools = mcp_tools_to_gemini_tools(
            mcp_result.tools
        )

        task = os.getenv("AGENT_TASK")

        if not task:
            with open("events/pipeline_failure.json", "r") as file:
                pipeline_event = json.load(file)

            task = (
                "A CI/CD pipeline has failed. "
                "Investigate the failure using the available tools. "
                "Determine the likely root cause and recommend recovery steps.\n\n"
                f"CI/CD Event:\n{json.dumps(pipeline_event, indent=2)}"
            )

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=task,
            tools=gemini_tools,
        )

        # Agentic loop
        while True:

            function_results = []

            for step in interaction.steps:

                if step.type == "function_call":

                    print(f"\nGemini requested tool: {step.name}")
                    print(f"Arguments: {step.arguments}")

                    # Call the MCP tool
                    tool_result = await mcp_client.call_tool(
                        step.name,
                        step.arguments or {},
                    )

                    print(f"MCP tool result: {tool_result}")

                    result_text = mcp_result_to_text(
                        tool_result
                    )

                    function_results.append(
                        {
                            "type": "function_result",
                            "name": step.name,
                            "call_id": step.id,
                            "result": [
                                {
                                    "type": "text",
                                    "text": result_text,
                                }
                            ],
                        }
                    )

            # Gemini didn't request another tool
            if not function_results:
                break

            # Send MCP results back to Gemini
            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                previous_interaction_id=interaction.id,
                input=function_results,
                tools=gemini_tools,
            )

        print("\nFinal response:")
        print(interaction.output_text)


asyncio.run(main())
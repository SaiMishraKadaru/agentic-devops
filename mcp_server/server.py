from mcp.server import MCPServer

from tools.devops_tools import (
    container_status,
    container_logs,
)

mcp = MCPServer("Agentic DevOps Server")


@mcp.tool()
def get_container_status():
    """Get the current status of the agentic-devops-demo Docker container."""
    return container_status("agentic-devops-demo")


@mcp.tool()
def get_container_logs():
    """Get recent logs from the agentic-devops-demo Docker container."""
    return container_logs("agentic-devops-demo")


if __name__ == "__main__":
    mcp.run()
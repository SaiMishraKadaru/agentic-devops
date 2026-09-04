from mcp.server import MCPServer

from tools.devops_tools import (
    get_deployment_status,
    get_deployment_logs,
)


mcp = MCPServer("Agentic DevOps Server")


@mcp.tool()
def deployment_status():
    """Get the current status of the payment-api deployment."""

    return get_deployment_status()


@mcp.tool()
def deployment_logs():
    """Get the recent logs from the payment-api deployment."""

    return get_deployment_logs()


if __name__ == "__main__":
    mcp.run()   
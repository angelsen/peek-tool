"""MCP server app instance for peek-tool.

This module contains the FastMCP application instance used across the MCP server components.
"""

from mcp.server.fastmcp import FastMCP

# Create the server instance with concise name and clear description
mcp = FastMCP(
    name="Peek",
    description="Inspect and explore code and data structures",
    instructions="Inspect Python modules, classes, methods, functions, and JSON files to understand their structure.",
)

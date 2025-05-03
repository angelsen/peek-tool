"""MCP server package for peek-tool.

This package provides an MCP server that exposes peek functionality
through the Model Context Protocol, allowing LLMs to inspect Python modules.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Peek",
    description="Inspect and explore code and data structures",
    instructions="Inspect Python modules, classes, methods, functions, and JSON files to understand their structure.",
)

import peek_tool.mcp_server.tools  # noqa: F401, E402
import peek_tool.mcp_server.resources  # noqa: F401, E402
import peek_tool.mcp_server.prompts  # noqa: F401, E402

__all__ = ["mcp"]


def main():
    """Entry point for the MCP server."""
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Run the Peek MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)",
    )

    args = parser.parse_args()
    mcp.run(transport=args.transport)


# Make the module callable for the entry point
if __name__ == "__main__":
    main()

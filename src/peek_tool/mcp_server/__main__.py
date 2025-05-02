"""MCP server entry point for peek-tool.

This module provides the main entry point for running the peek MCP server.
"""

import argparse
from typing import List, Optional

from mcp.server.fastmcp.server import FastMCP

from peek_tool.mcp_server.tools import register_tools
from peek_tool.mcp_server.resources import register_resources
from peek_tool.mcp_server.prompts import register_prompts


def create_server(
    name: str = "Peek",
    instructions: str = "Inspect Python modules, classes, methods, functions, and JSON files to understand their structure.",
) -> FastMCP:
    """Create and configure a FastMCP server for peek-tool."""
    # Create the server instance with concise name and clear description
    app = FastMCP(
        name=name,
        instructions=instructions,
        description="Inspect and explore code and data structures",
    )

    # Register components
    register_tools(app)
    register_resources(app)
    register_prompts(app)

    return app


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Peek MCP server")

    parser.add_argument(
        "--name",
        default="Peek",
        help="The name of the server (default: 'Peek')",
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the peek MCP server."""
    parsed_args = parse_args(args)

    # Create the server
    app = create_server(name=parsed_args.name)

    # Run with the specified transport
    app.run(transport=parsed_args.transport)


if __name__ == "__main__":
    main()

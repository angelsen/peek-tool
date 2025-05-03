"""MCP server package for peek-tool.

This package provides an MCP server that exposes peek functionality
through the Model Context Protocol, allowing LLMs to inspect Python modules.
"""

from peek_tool.mcp_server.app import app

# Import tools and resources to register them with the app
import peek_tool.mcp_server.tools  # noqa: F401
import peek_tool.mcp_server.resources  # noqa: F401

__all__ = ["app"]


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
    app.run(transport=args.transport)


# Make the module callable for the entry point
if __name__ == "__main__":
    main()

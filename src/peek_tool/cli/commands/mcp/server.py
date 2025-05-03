"""MCP server command implementation."""

import typer

from peek_tool.mcp_server import server


def server_command(
    transport: str = typer.Option(
        "stdio", "--transport", "-t", help="Transport protocol (stdio, sse)"
    ),
) -> None:
    """Start the MCP server for integration."""
    try:
        # Run the MCP server with specified options
        server.run(transport=transport)
    except Exception as e:
        typer.secho(
            f"Error starting MCP server: {str(e)}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(code=1)

"""MCP server command implementation."""

import typer


def server_command(
    name: str = typer.Option("Peek", "--name", "-n", help="Server name"),
    transport: str = typer.Option(
        "stdio", "--transport", "-t", help="Transport protocol (stdio, sse)"
    ),
) -> None:
    """Start the MCP server for integration."""
    try:
        # Import here to avoid circular imports
        from peek_tool.mcp_server.__main__ import main as mcp_server_main

        # Start the MCP server with proper arguments
        mcp_server_main(["--name", name, "--transport", transport])

    except Exception as e:
        typer.secho(
            f"Error starting MCP server: {str(e)}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(code=1)

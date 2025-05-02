"""MCP command group for the peek CLI."""

import typer
from peek_tool.cli.commands.mcp.init import init_command
from peek_tool.cli.commands.mcp.server import server_command

app = typer.Typer(help="MCP server and integration commands")

# Register commands
app.command("init")(init_command)
app.command("server")(server_command)

__all__ = ["app"]

"""CLI app instance for peek-tool.

This module contains the Typer application instance used across the CLI components.
"""

import typer
from typing import Optional

# Import command groups and commands
from peek_tool.cli.commands.mcp import app as mcp_app
from peek_tool.cli.commands.inspect.command import inspect_command

app = typer.Typer(
    help="Peek: Inspect Python modules, APIs, and data files",
    no_args_is_help=True,
)

# Register command groups
app.add_typer(mcp_app, name="mcp")

# Register direct commands
app.command("inspect")(inspect_command)


# Default callback to show help when no command is provided
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Peek tool for inspecting Python modules and JSON files."""
    if ctx.invoked_subcommand is None:
        # Show help by default
        typer.echo(ctx.get_help())


# Default command to handle the shorthand 'peek <module>'
@app.command(name="", hidden=True)
def default_command(
    target: str = typer.Argument(..., help="Target to inspect"),
    type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Type of target to inspect"
    ),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format"),
):
    """Default command that acts as an alias for the inspect command."""
    # Execute the inspect command directly
    inspect_command(target=target, type=type, format=format)


if __name__ == "__main__":
    app()

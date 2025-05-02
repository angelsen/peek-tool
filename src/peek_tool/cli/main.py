"""Main CLI entry point for peek-tool."""

import typer
from typing import Optional

from peek_tool.cli.commands import inspect_command, mcp_command

# Main Typer app
app = typer.Typer(
    help="Peek: Inspect Python modules, APIs, and data files",
    no_args_is_help=True,
)

# MCP subcommand group
mcp_app = typer.Typer(help="MCP server and integration commands")
app.add_typer(mcp_app, name="mcp")


@app.command("inspect")
def inspect_command_handler(
    target: str = typer.Argument(
        ..., help="Target to inspect (e.g., Python module, class, or file path)"
    ),
    type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Type of target to inspect (auto-detected if not specified)",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format (auto-selected based on target if not specified)",
    ),
):
    """Inspect a Python module, class, method, function, or JSON file."""

    # Create a compatible args object for the existing command handler
    class Args:
        pass

    args = Args()
    args.target = target
    args.type = type
    args.format = format

    inspect_command.execute(args)


@mcp_app.command("init")
def mcp_init_command(
    target: str = typer.Option(
        None,
        "--target",
        "-t",
        help="Target integration platform (cursor, claude, custom)",
    ),
    scope: str = typer.Option(
        None, "--scope", "-s", help="Configuration scope (project, global)"
    ),
    name: str = typer.Option(None, "--name", "-n", help="Name for the configuration"),
    package_manager: str = typer.Option(
        None, "--package-manager", "-p", help="Package manager to use (uv, pip)"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i/-I", help="Run in interactive mode"
    ),
):
    """Initialize MCP configuration for integration platforms."""

    # Create a compatible args object for the existing command handler
    class Args:
        pass

    args = Args()
    args.interactive = interactive

    # Only set these attrs if they were explicitly provided
    if target is not None:
        args.target = target
    if scope is not None:
        args.scope = scope
    if name is not None:
        args.name = name
    if package_manager is not None:
        args.package_manager = package_manager

    args.mcp_command = "init"

    mcp_command.execute_init(args)


@mcp_app.command("server")
def mcp_server_command(
    name: str = typer.Option("Peek", "--name", "-n", help="Server name"),
    transport: str = typer.Option(
        "stdio", "--transport", "-t", help="Transport protocol (stdio, sse)"
    ),
):
    """Start the MCP server for integration."""

    # Create a compatible args object for the existing command handler
    class Args:
        pass

    args = Args()
    args.name = name
    args.transport = transport
    args.mcp_command = "server"

    mcp_command.execute_server(args)


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

    # Create an Args object for the inspect command
    class Args:
        pass

    args = Args()
    args.target = target
    args.type = type
    args.format = format

    # Execute the inspect command
    inspect_command.execute(args)


if __name__ == "__main__":
    app()

"""MCP initialization command."""

from typing import Optional

import typer

# Importing the utility functions from the original mcp_command module
from peek_tool.cli.commands.mcp.utils import (
    init_cursor_config,
    init_claude_config,
    init_custom_config,
)


def init_command(
    target: Optional[str] = typer.Option(
        None,
        "--target",
        "-t",
        help="Target integration platform (cursor, claude, custom)",
    ),
    scope: Optional[str] = typer.Option(
        None, "--scope", "-s", help="Configuration scope (project, global)"
    ),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Name for the configuration"
    ),
    package_manager: Optional[str] = typer.Option(
        None, "--package-manager", "-p", help="Package manager to use (uv, pip)"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i/-I", help="Run in interactive mode"
    ),
) -> None:
    """Initialize MCP configuration for integration platforms."""
    try:
        # If interactive mode is enabled and target is not specified
        if interactive:
            if not target:
                targets = ["cursor", "claude", "custom"]
                target_descriptions = ["Cursor IDE", "Claude Desktop", "Custom setup"]

                for i, (t, desc) in enumerate(zip(targets, target_descriptions), 1):
                    typer.echo(f"{i}. {desc}")

                target_index = (
                    typer.prompt("Select integration platform", type=int, default=1) - 1
                )

                if 0 <= target_index < len(targets):
                    target = targets[target_index]
                else:
                    target = "cursor"

            if not scope:
                scopes = ["project", "global"]
                scope_descriptions = [
                    "Project (local to this project)",
                    "Global (available in all projects)",
                ]

                typer.echo("")  # Empty line for better spacing
                for i, (s, desc) in enumerate(zip(scopes, scope_descriptions), 1):
                    typer.echo(f"{i}. {desc}")

                scope_index = (
                    typer.prompt("Select configuration scope", type=int, default=1) - 1
                )
                scope = (
                    scopes[scope_index] if 0 <= scope_index < len(scopes) else "project"
                )

            if not name:
                name = typer.prompt(
                    "Enter a name for this configuration", default="peek"
                )

            if not package_manager:
                pms = ["uv", "pip"]
                pm_descriptions = ["uv (recommended)", "pip"]

                typer.echo("")  # Empty line for better spacing
                for i, (pm, desc) in enumerate(zip(pms, pm_descriptions), 1):
                    typer.echo(f"{i}. {desc}")

                pm_index = (
                    typer.prompt("Select package manager", type=int, default=1) - 1
                )
                package_manager = pms[pm_index] if 0 <= pm_index < len(pms) else "uv"

        # Process based on selected target
        if target == "cursor":
            init_cursor_config(target, scope, name, package_manager)
        elif target == "claude":
            init_claude_config(target, scope, name, package_manager)
        else:
            init_custom_config(target, scope, name, package_manager, interactive)

    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

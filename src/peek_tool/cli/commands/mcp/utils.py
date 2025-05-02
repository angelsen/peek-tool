"""Utility functions for MCP commands."""

import json
import os
import sys
from pathlib import Path

import typer


def init_cursor_config(
    target: str, scope: str, name: str, package_manager: str
) -> None:
    """Initialize Cursor MCP configuration."""
    # Determine config directory and file path
    if scope == "project":
        config_dir = Path(".cursor")
        config_file = config_dir / "mcp.json"
    else:  # Global scope
        config_dir = Path.home() / ".cursor"
        config_file = config_dir / "mcp.json"

    # Create config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Determine the command and args based on package manager
    if package_manager == "uv":
        command = "uv"
        command_args = ["run", "peek-mcp"]
    else:  # pip
        command = "python"
        command_args = ["-m", "peek_tool.mcp_server"]

    # Prepare the configuration
    server_config = {"command": command, "args": command_args, "env": {}}

    # Load existing config if it exists
    config = {"mcpServers": {}}
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                if "mcpServers" not in config:
                    config["mcpServers"] = {}
        except json.JSONDecodeError:
            typer.secho(
                f"Warning: Existing config file {config_file} is not valid JSON. Creating new file.",
                fg=typer.colors.YELLOW,
                err=True,
            )

    # Add or update server configuration
    config["mcpServers"][name] = server_config

    # Write the configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    typer.secho("\n✓ Success!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Cursor MCP configuration created at: {config_file}")
    typer.echo(f"Server '{name}' configured with {package_manager} as package manager")

    # Instructions for Cursor usage
    typer.secho("\nUsage Instructions:", fg=typer.colors.BLUE, bold=True)
    typer.echo("1. Open Cursor AI")
    typer.echo("2. Type a command that can use the Peek tool")
    typer.echo("3. If asked, approve the tool usage")


def init_claude_config(
    target: str, scope: str, name: str, package_manager: str
) -> None:
    """Initialize Claude MCP configuration."""
    # Determine paths based on OS
    if sys.platform == "darwin":  # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "Claude"
        config_file = config_dir / "claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        appdata = Path(os.environ.get("APPDATA", ""))
        config_dir = appdata / "Claude"
        config_file = config_dir / "claude_desktop_config.json"
    else:  # Linux and others
        config_dir = Path.home() / ".config" / "Claude"
        config_file = config_dir / "claude_desktop_config.json"

    # Create config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Determine command based on package manager
    if package_manager == "uv":
        command = "uv"
        command_args = ["run", "peek-mcp"]
    else:  # pip
        command = "python"
        command_args = ["-m", "peek_tool.mcp_server"]

    # Load existing config or create new
    config = {"mcpServers": {}}
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                if "mcpServers" not in config:
                    config["mcpServers"] = {}
        except json.JSONDecodeError:
            typer.secho(
                f"Warning: Existing config file {config_file} is not valid JSON. Creating new file.",
                fg=typer.colors.YELLOW,
                err=True,
            )

    # Add or update server configuration
    config["mcpServers"][name] = {
        "command": command,
        "args": command_args,
        "env": {},
    }

    # Write configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    typer.secho("\n✓ Success!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Claude MCP configuration created at: {config_file}")
    typer.echo(f"Server '{name}' configured with {package_manager} as package manager")

    # Instructions for Claude usage
    typer.secho("\nUsage Instructions:", fg=typer.colors.BLUE, bold=True)
    typer.echo("1. Restart Claude Desktop if it's running")
    typer.echo("2. Look for the hammer icon in the message input area")
    typer.echo("3. Click the hammer to view available tools")
    typer.echo("4. Ask Claude to use the Peek tool")


def init_custom_config(
    target: str, scope: str, name: str, package_manager: str, interactive: bool = True
) -> None:
    """Initialize custom MCP configuration."""
    # Get configuration file path
    default_path = str(
        Path(".mcp.json") if scope == "project" else Path.home() / ".mcp.json"
    )

    file_path = default_path
    command = ""
    command_args = []
    env_vars = {}

    if interactive:
        typer.secho(
            "\nCustom MCP Configuration", fg=typer.colors.BRIGHT_BLUE, bold=True
        )
        typer.secho("---------------------", fg=typer.colors.BRIGHT_BLUE)

        file_path = typer.prompt("Configuration file path", default=default_path)

        # Get custom command
        command = typer.prompt("Command to run the MCP server")

        # Get command arguments
        args_str = typer.prompt("Command arguments (space-separated)", default="")
        command_args = args_str.split() if args_str else []

        # Environment variables
        add_env = typer.confirm("Add environment variables?", default=False)

        while add_env:
            env_key = typer.prompt("Environment variable name")
            env_val = typer.prompt(f"Value for {env_key}")
            env_vars[env_key] = env_val

            add_env = typer.confirm("Add another environment variable?", default=False)

    config_file = Path(file_path)

    # Load existing config or create new
    config = {"mcpServers": {}}
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                if "mcpServers" not in config:
                    config["mcpServers"] = {}
        except json.JSONDecodeError:
            typer.secho(
                f"Warning: Existing config file {config_file} is not valid JSON. Creating new file.",
                fg=typer.colors.YELLOW,
                err=True,
            )

    # Add or update server configuration
    config["mcpServers"][name] = {
        "command": command,
        "args": command_args,
        "env": env_vars,
    }

    # Ensure directory exists
    os.makedirs(config_file.parent, exist_ok=True)

    # Write configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    typer.secho("\n✓ Success!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Custom MCP configuration created at: {config_file}")
    typer.echo(f"Server '{name}' configured with custom settings")

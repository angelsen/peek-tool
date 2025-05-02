"""MCP integration commands for peek-tool."""

import json
import os
import sys
from pathlib import Path

import typer


def execute_server(args):
    """Execute the MCP server command."""
    try:
        # Import here to avoid circular imports
        from peek_tool.mcp_server.__main__ import main as mcp_server_main

        # Prepare args for the MCP server
        mcp_args = ["--name", args.name, "--transport", args.transport]

        # Start the MCP server
        mcp_server_main(mcp_args)
        return 0
    except Exception as e:
        typer.secho(
            f"Error starting MCP server: {str(e)}", fg=typer.colors.RED, err=True
        )
        return 1


def execute_init(args):
    """Execute the MCP initialization command."""
    try:
        # Check if we should run in interactive mode (default) or with provided arguments
        if not hasattr(args, "interactive") or args.interactive:
            return interactive_init()

        # Non-interactive mode with direct arguments
        if args.target == "cursor":
            return init_cursor_config(args)
        elif args.target == "claude":
            return init_claude_config(args)
        else:
            typer.secho(
                f"Unsupported target: {args.target}", fg=typer.colors.RED, err=True
            )
            return 1
    except Exception as e:
        typer.secho(
            f"Error initializing MCP configuration: {str(e)}",
            fg=typer.colors.RED,
            err=True,
        )
        return 1


def interactive_init():
    """Interactive MCP initialization using Typer prompts."""
    typer.secho("Peek MCP Configuration Wizard", fg=typer.colors.BRIGHT_BLUE, bold=True)
    typer.secho("=============================", fg=typer.colors.BRIGHT_BLUE)

    # Target platform selection
    targets = ["cursor", "claude", "custom"]
    target_descriptions = ["Cursor IDE", "Claude Desktop", "Custom setup"]

    for i, (target, desc) in enumerate(zip(targets, target_descriptions), 1):
        typer.echo(f"{i}. {desc}")

    target_index = typer.prompt("Select integration platform", type=int, default=1) - 1
    target = targets[target_index] if 0 <= target_index < len(targets) else "cursor"

    # Scope selection
    scopes = ["project", "global"]
    scope_descriptions = [
        "Project (local to this project)",
        "Global (available in all projects)",
    ]

    typer.echo("")  # Empty line for better spacing
    for i, (scope, desc) in enumerate(zip(scopes, scope_descriptions), 1):
        typer.echo(f"{i}. {desc}")

    scope_index = typer.prompt("Select configuration scope", type=int, default=1) - 1
    scope = scopes[scope_index] if 0 <= scope_index < len(scopes) else "project"

    # Configuration name
    name = typer.prompt("Enter a name for this configuration", default="peek")

    # Package manager
    pms = ["uv", "pip"]
    pm_descriptions = ["uv (recommended)", "pip"]

    typer.echo("")  # Empty line for better spacing
    for i, (pm, desc) in enumerate(zip(pms, pm_descriptions), 1):
        typer.echo(f"{i}. {desc}")

    pm_index = typer.prompt("Select package manager", type=int, default=1) - 1
    package_manager = pms[pm_index] if 0 <= pm_index < len(pms) else "uv"

    # Create args object for specific initializers
    class Args:
        pass

    args = Args()
    args.target = target
    args.scope = scope
    args.name = name
    args.package_manager = package_manager

    # Call the appropriate initializer
    if target == "cursor":
        return init_cursor_config(args)
    elif target == "claude":
        return init_claude_config(args)
    else:
        return init_custom_config(args)


def init_cursor_config(args):
    """Initialize Cursor MCP configuration."""
    # Determine config directory and file path
    if args.scope == "project":
        config_dir = Path(".cursor")
        config_file = config_dir / "mcp.json"
    else:  # Global scope
        config_dir = Path.home() / ".cursor"
        config_file = config_dir / "mcp.json"

    # Create config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Determine the command and args based on package manager
    if args.package_manager == "uv":
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
    config["mcpServers"][args.name] = server_config

    # Write the configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    typer.secho("\n✓ Success!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Cursor MCP configuration created at: {config_file}")
    typer.echo(
        f"Server '{args.name}' configured with {args.package_manager} as package manager"
    )

    # Instructions for Cursor usage
    typer.secho("\nUsage Instructions:", fg=typer.colors.BLUE, bold=True)
    typer.echo("1. Open Cursor AI")
    typer.echo("2. Type a command that can use the Peek tool")
    typer.echo("3. If asked, approve the tool usage")

    return 0


def init_claude_config(args):
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
    if args.package_manager == "uv":
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
    config["mcpServers"][args.name] = {
        "command": command,
        "args": command_args,
        "env": {},
    }

    # Write configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    typer.secho("\n✓ Success!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Claude MCP configuration created at: {config_file}")
    typer.echo(
        f"Server '{args.name}' configured with {args.package_manager} as package manager"
    )

    # Instructions for Claude usage
    typer.secho("\nUsage Instructions:", fg=typer.colors.BLUE, bold=True)
    typer.echo("1. Restart Claude Desktop if it's running")
    typer.echo("2. Look for the hammer icon in the message input area")
    typer.echo("3. Click the hammer to view available tools")
    typer.echo("4. Ask Claude to use the Peek tool")

    return 0


def init_custom_config(args):
    """Initialize custom MCP configuration."""
    typer.secho("\nCustom MCP Configuration", fg=typer.colors.BRIGHT_BLUE, bold=True)
    typer.secho("---------------------", fg=typer.colors.BRIGHT_BLUE)

    # Get configuration file path
    default_path = str(
        Path(".mcp.json") if args.scope == "project" else Path.home() / ".mcp.json"
    )
    file_path = typer.prompt("Configuration file path", default=default_path)
    config_file = Path(file_path)

    # Get custom command
    command = typer.prompt("Command to run the MCP server")

    # Get command arguments
    args_str = typer.prompt("Command arguments (space-separated)", default="")
    command_args = args_str.split() if args_str else []

    # Environment variables
    env_vars = {}
    add_env = typer.confirm("Add environment variables?", default=False)

    while add_env:
        env_key = typer.prompt("Environment variable name")
        env_val = typer.prompt(f"Value for {env_key}")
        env_vars[env_key] = env_val

        add_env = typer.confirm("Add another environment variable?", default=False)

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
    config["mcpServers"][args.name] = {
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
    typer.echo(f"Server '{args.name}' configured with custom settings")

    return 0

"""MCP integration commands for peek-tool."""

import json
import os
import sys
from pathlib import Path


def register_arguments(parser):
    """Register arguments for the MCP commands."""
    subparsers = parser.add_subparsers(
        dest="mcp_command", help="MCP command to execute"
    )

    # Add server command
    server_parser = subparsers.add_parser("server", help="Start the MCP server")
    server_parser.add_argument(
        "--name", default="Peek", help="The name of the server (default: 'Peek')"
    )
    server_parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)",
    )

    # Add init command for Cursor integration
    init_parser = subparsers.add_parser("init", help="Initialize MCP configuration")
    init_parser.add_argument(
        "--target",
        choices=["cursor", "claude"],
        required=True,
        help="Target integration platform",
    )
    init_parser.add_argument(
        "--scope",
        choices=["project", "global"],
        default="project",
        help="Configuration scope (project or global)",
    )
    init_parser.add_argument(
        "--name", default="peek", help="Name for the MCP server configuration"
    )
    init_parser.add_argument(
        "--package-manager",
        choices=["uv", "pip"],
        default="uv",
        help="Package manager to use (default: uv)",
    )


def execute(args):
    """Execute the MCP command."""
    if args.mcp_command == "server":
        return execute_server(args)
    elif args.mcp_command == "init":
        return execute_init(args)
    else:
        print(
            "Please specify an MCP command. Use --help for more information.",
            file=sys.stderr,
        )
        return 1


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
        print(f"Error starting MCP server: {str(e)}", file=sys.stderr)
        return 1


def execute_init(args):
    """Execute the MCP initialization command."""
    try:
        if args.target == "cursor":
            return init_cursor_config(args)
        elif args.target == "claude":
            print("Claude initialization not yet implemented.")
            return 1
        else:
            print(f"Unsupported target: {args.target}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Error initializing MCP configuration: {str(e)}", file=sys.stderr)
        return 1


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
            print(
                f"Warning: Existing config file {config_file} is not valid JSON. Creating new file.",
                file=sys.stderr,
            )

    # Add or update server configuration
    config["mcpServers"][args.name] = server_config

    # Write the configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Cursor MCP configuration created at: {config_file}")
    print(
        f"Server '{args.name}' configured with {args.package_manager} as package manager"
    )
    return 0

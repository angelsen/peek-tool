"""Main CLI entry point for peek-tool."""

import argparse
import sys

from peek_tool.cli.commands import inspect_command, mcp_command


def main():
    """Entry point for the peek CLI."""
    parser = argparse.ArgumentParser(
        description="Peek: Inspect Python modules, APIs, and data files"
    )

    # Check if the first argument is a special keyword command
    if len(sys.argv) > 1:
        # Handle mcpinit as a special command
        if sys.argv[1] == "mcpinit":
            # Set up args for cursor init with project scope
            init_args = argparse.Namespace()
            init_args.mcp_command = "init"
            init_args.target = "cursor"
            init_args.scope = "project"
            init_args.name = "peek"
            init_args.package_manager = "uv"
            return mcp_command.execute_init(init_args)

        # Check if the first argument might be a module to inspect
        # (not starting with - and not a known command)
        if not sys.argv[1].startswith("-") and sys.argv[1] not in ["inspect", "mcp"]:
            # Treat as a target for inspection
            inspect_args = argparse.Namespace()
            inspect_args.target = sys.argv[1]
            inspect_args.type = None
            inspect_args.format = None

            # Add any additional flags if present
            for i in range(2, len(sys.argv)):
                if sys.argv[i] == "--type" or sys.argv[i] == "-t":
                    if i + 1 < len(sys.argv):
                        inspect_args.type = sys.argv[i + 1]
                elif sys.argv[i] == "--format" or sys.argv[i] == "-f":
                    if i + 1 < len(sys.argv):
                        inspect_args.format = sys.argv[i + 1]

            return inspect_command.execute(inspect_args)

    # Regular command line parsing for explicit commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Register the inspect command
    inspect_parser = subparsers.add_parser(
        "inspect", help="Inspect a Python module, class, or JSON file"
    )
    inspect_command.register_arguments(inspect_parser)

    # Register the MCP commands
    mcp_parser = subparsers.add_parser(
        "mcp", help="MCP server and integration commands"
    )
    mcp_command.register_arguments(mcp_parser)

    # Parse arguments
    args = parser.parse_args()

    # Dispatch to the appropriate command
    try:
        if args.command == "inspect":
            return inspect_command.execute(args)
        elif args.command == "mcp":
            return mcp_command.execute(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


# Entry point for the CLI
app = main

if __name__ == "__main__":
    sys.exit(main())

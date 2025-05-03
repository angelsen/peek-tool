"""Inspect command implementation for peek-tool."""

import typer

from peek_tool.core.base import InspectorFactory


def inspect_command(
    target: str = typer.Argument(
        ..., help="Target to inspect (e.g., Python module, class, or file path)"
    ),
) -> None:
    """Inspect a Python module, class, method, function, or JSON file."""
    try:
        # Perform inspection using the factory
        output = InspectorFactory.inspect(target)

        # Print the formatted output
        typer.echo(output)

    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

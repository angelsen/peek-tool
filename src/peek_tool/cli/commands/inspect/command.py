"""Inspect command implementation for peek-tool."""

from pathlib import Path
from typing import Optional

import typer

from peek_tool.core.base import InspectorFactory
from peek_tool.formatters.base import FormatterFactory


def auto_detect_type(target: str) -> str:
    """Auto-detect the type of target based on its characteristics."""
    # Check if it's a file path with extension
    path = Path(target.split(":")[0] if ":" in target else target)
    if path.exists() and path.is_file():
        extension = path.suffix.lower()
        if extension == ".json":
            return "json"
        # Add more file types as needed

    # Default to Python for other targets
    return "python"


def get_default_format(target_type: str) -> str:
    """Get the default format based on target type."""
    format_mapping = {
        "python": "text",
        "json": "json-text",
        # Add more mappings as needed
    }

    return format_mapping.get(target_type, "text")


def inspect_command(
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
) -> None:
    """Inspect a Python module, class, method, function, or JSON file."""
    try:
        # Auto-detect target type if not specified
        target_type = type or auto_detect_type(target)

        # Auto-select format if not specified
        format_type = format or get_default_format(target_type)

        # Create the appropriate inspector
        inspector = InspectorFactory.create_inspector(target_type)

        # Check if the inspector supports the target
        if not inspector.supports(target):
            typer.secho(
                f"Error: Target '{target}' is not supported by the {target_type} inspector",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)

        # Perform the inspection
        result = inspector.inspect(target)

        # Format the results
        formatter = FormatterFactory.create_formatter(format_type)
        output = formatter.format(result)

        # Print the output
        typer.echo(output)

    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

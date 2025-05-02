"""Inspect command for the peek CLI."""

from pathlib import Path

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


def execute(args):
    """Execute the inspect command."""
    try:
        # Auto-detect target type if not specified
        target_type = args.type
        if not target_type:
            target_type = auto_detect_type(args.target)

        # Auto-select format if not specified
        format_type = args.format
        if not format_type:
            format_type = get_default_format(target_type)

        # Create the appropriate inspector
        inspector = InspectorFactory.create_inspector(target_type)

        # Check if the inspector supports the target
        if not inspector.supports(args.target):
            typer.secho(
                f"Error: Target '{args.target}' is not supported by the {target_type} inspector",
                fg=typer.colors.RED,
                err=True,
            )
            return 1

        # Perform the inspection
        result = inspector.inspect(args.target)

        # Format the results
        formatter = FormatterFactory.create_formatter(format_type)
        output = formatter.format(result)

        # Print the output using typer
        typer.echo(output)
        return 0

    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED, err=True)
        return 1

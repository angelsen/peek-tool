"""Inspect command for the peek CLI."""

import sys
from pathlib import Path

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


def register_arguments(parser):
    """Register the arguments for the inspect command."""
    parser.add_argument(
        "target", help="Target to inspect (e.g., Python module, class, or file path)"
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=["python", "json"],  # Add more as implemented
        help="Type of target to inspect (auto-detected if not specified)",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "json-text"],  # Add more as implemented
        help="Output format (auto-selected based on target if not specified)",
    )


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
            print(
                f"Error: Target '{args.target}' is not supported by the {target_type} inspector",
                file=sys.stderr,
            )
            return 1

        # Perform the inspection
        result = inspector.inspect(args.target)

        # Format the results
        formatter = FormatterFactory.create_formatter(format_type)
        output = formatter.format(result)

        # Print the output
        print(output)
        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

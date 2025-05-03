"""MCP server tools for peek-tool.

This module contains the tool definitions used by the peek MCP server.
"""

from pathlib import Path
from typing import Optional, Annotated
from pydantic import Field

from mcp.server.fastmcp import Context

from peek_tool.core.base import InspectorFactory
from peek_tool.formatters.base import FormatterFactory
from peek_tool.mcp_server.app import mcp


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


@mcp.tool()
def inspect_module(
    target: Annotated[
        str,
        Field(
            description="Target to inspect (e.g., a Python module, class name, or JSON file path)"
        ),
    ],
    inspector_type: Annotated[
        Optional[str],
        Field(
            description="Type of inspector to use (python or json, auto-detected if not specified)"
        ),
    ] = None,
    output_format: Annotated[
        Optional[str],
        Field(
            description="Output format (text or json-text, auto-selected if not specified)"
        ),
    ] = None,
    ctx: Optional[Context] = None,
) -> str:
    """Inspect a Python module, class, method, function, or JSON file.

    Returns the detailed structure and documentation of the target.

    Examples:
      - `inspect_module(target="json")` - Inspect the json module
      - `inspect_module(target="json.JSONEncoder")` - Inspect a class
      - `inspect_module(target="json.dumps")` - Inspect a function
      - `inspect_module(target="/path/to/file.json")` - Inspect a JSON file
    """
    try:
        # Auto-detect target type if not specified
        target_type = inspector_type
        if not target_type:
            target_type = auto_detect_type(target)
            if ctx:
                ctx.info(f"Auto-detected target type: {target_type}")

        # Auto-select format if not specified
        format_type = output_format
        if not format_type:
            format_type = get_default_format(target_type)
            if ctx:
                ctx.info(f"Auto-selected format: {format_type}")

        # Report start of inspection
        if ctx:
            ctx.info(f"Inspecting {target} using {target_type} inspector")

        # Create the appropriate inspector
        inspector = InspectorFactory.create_inspector(target_type)

        # Check if the inspector supports the target
        if not inspector.supports(target):
            error_msg = f"Error: Target '{target}' is not supported by the {target_type} inspector"
            if ctx:
                ctx.error(error_msg)
            return error_msg

        # Perform the inspection
        result = inspector.inspect(target)

        # Format the results
        formatter = FormatterFactory.create_formatter(format_type)
        output = formatter.format(result)

        # Report completion
        if ctx:
            ctx.info(f"Inspection of {target} completed successfully")

        return output

    except Exception as e:
        error_msg = f"Error inspecting {target}: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg

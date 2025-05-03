"""MCP server tools for peek-tool.

This module contains the tool definitions used by the peek MCP server.
"""

from typing import Optional, Annotated
from pydantic import Field

from mcp.server.fastmcp import Context

from peek_tool.core.base import InspectorFactory
from peek_tool.mcp_server.app import mcp


@mcp.tool()
def inspect_module(
    target: Annotated[
        str,
        Field(
            description="Target to inspect (e.g., a Python module, class name, or JSON file path)"
        ),
    ],
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
        # Log inspection details if context is provided
        if ctx:
            detected_type = InspectorFactory.detect_inspector_type(target)
            format_type = InspectorFactory.get_formatter_for_inspector(detected_type)
            ctx.info(
                f"Inspecting {target} (type: {detected_type}, format: {format_type})"
            )

        # Perform the inspection
        output = InspectorFactory.inspect(target)

        # Report completion
        if ctx:
            ctx.info(f"Inspection of {target} completed successfully")

        return output

    except Exception as e:
        error_msg = f"Error inspecting {target}: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg

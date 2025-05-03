"""MCP server tools for peek-tool."""

from typing import Optional, Annotated
from pydantic import Field

from mcp.server.fastmcp import Context

from peek_tool.core.base import InspectorFactory
from peek_tool.core.docstring_utils import DocstringExtractor
from peek_tool.mcp_server import server


@server.tool()
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


@server.tool()
def inspect_docstring(
    target: Annotated[
        str,
        Field(
            description="Target to get docstring for (e.g., 'json', 'json.JSONEncoder', 'json.dumps')"
        ),
    ],
    page: Annotated[
        int,
        Field(
            description="Page number (0-indexed) for paginated output",
            ge=0,
        ),
    ] = 0,
    page_size: Annotated[
        int,
        Field(
            description="Number of lines per page",
            ge=5,
            le=100,
        ),
    ] = 20,
    ctx: Optional[Context] = None,
) -> str:
    """Get the complete docstring for a Python module, class, or function with pagination.

    Returns the full docstring with pagination controls when the content is long.

    Examples:
      - `inspect_docstring(target="requests")` - Get requests module docstring
      - `inspect_docstring(target="json.JSONEncoder", page=1)` - Get page 2
      - `inspect_docstring(target="pathlib.Path.glob", page_size=50)` - Custom page size
    """
    try:
        # Log operation if context is provided
        if ctx:
            ctx.info(
                f"Retrieving docstring for {target} (page {page + 1}, size {page_size})"
            )

        # Get the paginated docstring
        rendered_text, metadata = DocstringExtractor.get_paginated_docstring(
            target, page, page_size
        )

        # Report completion
        if ctx:
            pagination = metadata.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)
            ctx.info(
                f"Retrieved docstring for {target} (page {page + 1}/{total_pages})"
            )

        # Return just the formatted text
        return rendered_text
    except Exception as e:
        error_msg = f"Error retrieving docstring for {target}: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return f"Error: {str(e)}"

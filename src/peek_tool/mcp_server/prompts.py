"""MCP server prompts for peek-tool."""

from typing import Annotated, Optional
from pydantic import Field

from peek_tool.mcp_server import server


@server.prompt("module-inspect")
def module_inspect_prompt(
    target: Annotated[
        str,
        Field(
            description="The name of the module, class, function, or path to JSON file to inspect"
        ),
    ],
) -> str:
    """Inspect a Python module, class, function, or JSON file."""
    return f"Please inspect '{target}' and explain its key functionality, parameters, and usage patterns."


@server.prompt("docstring-view")
def docstring_view_prompt(
    target: Annotated[
        str,
        Field(
            description="The name of the module, class, function, or method to view docstring for"
        ),
    ],
    page: Annotated[
        Optional[int],
        Field(description="The page number to view (0-indexed)"),
    ] = None,
    page_size: Annotated[
        Optional[int],
        Field(description="The number of lines per page"),
    ] = None,
) -> str:
    """View the complete docstring for a Python element with pagination."""
    prompt = f"Please show me the complete docstring for '{target}'"

    if page is not None:
        prompt += f", starting at page {page + 1}"

    if page_size is not None:
        prompt += f" with {page_size} lines per page"

    prompt += "."

    return prompt

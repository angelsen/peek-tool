"""MCP server prompts for peek-tool.

This module contains the prompt definitions used by the peek MCP server.
"""

from typing import Annotated
from pydantic import Field

from peek_tool.mcp_server.app import mcp


@mcp.prompt()
def module_inspect_prompt(
    target: Annotated[
        str,
        Field(
            description="The name of the module, class, function, or path to JSON file to inspect"
        ),
    ],
    target_type: Annotated[
        str, Field(description="Type of target (module, class, function, method, json)")
    ] = "module",
) -> str:
    """Inspect a Python module, class, function, or JSON file.

    Creates a prompt that guides the LLM to explore and explain the key
    functionality, parameters, and usage patterns of the specified target.
    """
    return f"Please inspect the Python {target_type} named '{target}' and explain its key functionality, parameters, and usage patterns."

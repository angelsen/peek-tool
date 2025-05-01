"""MCP server prompts for peek-tool.

This module contains the prompt definitions used by the peek MCP server.
"""

from mcp.server.fastmcp.server import FastMCP


def register_prompts(app: FastMCP) -> None:
    """Register all peek prompts with the FastMCP server."""

    @app.prompt(
        name="inspect", description="Inspect a Python module, class, or function"
    )
    def module_inspect_prompt(target: str, target_type: str = "module") -> str:
        """
        Create a prompt to inspect a Python module, class or function.

        Args:
            target: The name of the module, class, or function to inspect
            target_type: Type of target (module, class, function, method)
        """
        return f"Please inspect the Python {target_type} named '{target}' and explain its key functionality, parameters, and usage patterns."

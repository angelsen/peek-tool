"""MCP server tools for peek-tool.

This module contains the tool definitions used by the peek MCP server.
"""

from typing import Optional

from mcp.server.fastmcp.server import FastMCP, Context

from peek_tool.core.base import InspectorFactory
from peek_tool.formatters.base import FormatterFactory


def register_tools(app: FastMCP) -> None:
    """Register all peek tools with the FastMCP server."""

    @app.tool(
        name="inspect_module",
        description="Inspect a Python module, class, method or function and return its structure",
    )
    def inspect_module(
        target: str,
        inspector_type: str = "python",
        output_format: str = "text",
        ctx: Optional[Context] = None,
    ) -> str:
        """
        Inspect a Python module, class, method or function.

        Args:
            target: Target to inspect (e.g., a Python module or class name)
            inspector_type: Type of inspector to use (default: python)
            output_format: Output format (default: text)
            ctx: MCP context for progress reporting (optional)

        Returns:
            The formatted inspection result as text
        """
        try:
            # Report start of inspection
            if ctx:
                ctx.info(f"Inspecting {target} using {inspector_type} inspector")

            # Create the appropriate inspector
            inspector = InspectorFactory.create_inspector(inspector_type)

            # Check if the inspector supports the target
            if not inspector.supports(target):
                return f"Error: Target '{target}' is not supported by the {inspector_type} inspector"

            # Perform the inspection
            result = inspector.inspect(target)

            # Format the results
            formatter = FormatterFactory.create_formatter(output_format)
            output = formatter.format(result)

            # Report completion
            if ctx:
                ctx.info(f"Inspection of {target} completed successfully")

            return output

        except Exception as e:
            error_msg = f"Error inspecting {target}: {str(e)}"
            if ctx:
                ctx.error(error_msg)
            return f"Error: {str(e)}"
